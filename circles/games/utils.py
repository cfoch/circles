import urllib
import urllib2
from urllib import unquote
from decimal import Decimal

from factors.factory import FactorFunctionsFactory
from factors.utils import valid_factor_name
from games.models import Game
from games.models import Payment
from games.models import Player


def paypal_get_payment_info(tx,at):
    success = False
    post_data = [('cmd', '_notify-synch'), ('tx', tx), ('at', at)]
    result = urllib2.urlopen('https://www.sandbox.paypal.com/cgi-bin/webscr', urllib.urlencode(post_data))
    content = result.read().split('\n')
    info = {}

    for each in content[1:]:
        try:
            key, value = each.split("=")
            info[key] = value
        except:
            pass
    if content[0].find('SUCCESS') >= 0:
        success = True

    return success, info

def deserialize_paypal_custom_data(data):
    data = unquote(data)
    l = data.split("=")
    dic = {}
    for i in range(0, len(l), 2):
        dic[l[i]] = l[i + 1]
    return dic

def paypal_save_payment_info(info):
    print(info)
    custom_data = deserialize_paypal_custom_data(info['custom'])
    payer_email = unquote(info['payer_email'])
    payment_gross = Decimal(info['payment_gross'])
    quantity = int(info['quantity'])
    paypal_txn_id = info['txn_id']
    game_id = custom_data['game_id']

    # Create player if not exists.
    try:
        player = Player.objects.get(paypal=payer_email)
    except:
        player = Player()
        player.paypal = payer_email
        print("HOLA")

    payment = Payment()
    payment.paypal_txn_id = paypal_txn_id
    payment.payment_gross = payment_gross
    payment.quantity = quantity
    payment.sequences_shown = 0
    payment.game = Game.objects.get(game_id=game_id)
    print(paypal_txn_id, payment_gross, quantity)
    payment.save()
    # Link payment to this player
    player.save()
    player.payments.add(payment)
    player.save()
    return True

    return False

class PaymentCalculator:
    """
    Calculates the payment which the player will pay to see one or more
    sequences.
    """

    # TODO: It would be nice to operate with only decimals.
    # We get a margin of error when we convert from 'float' to Decimal
    # or viceversa. However, this margin of error, seems too MINIMUM and seems
    # we should not worry about it.

    def __init__(self, n, game_pk):
        game = Game.objects.get(pk=game_pk)

        self.max_discount = float(game.max_discount)
        self.base_payment = float(game.base_payment)
        self.sequences_played = float(game.sequences.all().count())
        self.n_sequences = float(n)
        self.factors = self._getFactors(game)

    def get_price(self):
        """
        Calculates de price the player will pay per an amount of {n} sequences.
        """
        if self.factors is None:
            return self.emergency_price()
        average_factor = self._average_factor()
        return self._to_decimal(
            self.base_payment * self.n_sequences * average_factor)

    def emergency_price(self):
        """
        This function is used when no factors are registered.
        """
        return self._to_decimal(self.base_payment * self.n_sequences)

    def _average_factor(self):
        if self.n_sequences == 1:
            return 1.0
        total_weight = 0
        suma = 0
        for factor in self.factors:
            suma += factor["value"] * factor["weight"]
            total_weight += factor["weight"]
        return suma / total_weight

    def _to_decimal(self, float_number):
        rounded_float = round(float_number, 2)
        return Decimal(rounded_float).quantize(Decimal("0.00"))

    def _default_factor(self, multiplier):
        return 1 + self.max_discount * (multiplier - 1)

    def _getFactors(self, game):
        """
        Returns a list of factors values allowed by {game}, each one related to
        its respective weight.
        Returns a list of {"value": value, "weight": weight} elements.
        """
        factors = game.factors.all()
        factory = FactorFunctionsFactory(self)
        if not factors:
            return
        factors_list = []
        for factor in factors:
            name = factor.function_name
            if not valid_factor_name(name):
                return
            factor_function = getattr(factory, name)
            # Add the result and weight of the function which is a
            # {"value": value, "weight": weight}
            factors_list.append(factor_function())
        return factors_list
