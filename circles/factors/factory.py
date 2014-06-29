import datetime
import math

from factors.utils import factor_set_weight


class FactorFunctionsFactory:
    """
    Write payments-factor functions here!
    DO NOT change/delete a function at least the whole team agree.
    Functions/methods HAVE TO start with 'factor_'.
    If you need to write helper functions, write them in PaymentCalculator or
    in factors.utils.
    """

    def __init__(self, payment_calculator):
        self.calculator = payment_calculator

    @factor_set_weight(1)
    def factor_time(self):
        """
        It is the factor which discounts a maximum price of max_discount
        according time. When the time is closer to midnight, the discount is
        maximum. But, when the time is closer to noon, the discount is minimum
        or zero, so it means a factor of 1.0 .
        """
        # t: oscillate between 0 and 23
        t = datetime.datetime.now().hour
        multiplier = abs(math.sin(math.pi * t / 23))
        return self.calculator._default_factor(multiplier)

    @factor_set_weight(4)
    def factor_n(self):
        """
        It is the factor which discounts according {self.n_sequences}, which is
        the number of sequences the user wishes to see. The more this number of
        sequences is, the more the discount is. However, the less this number
        is, the less the discount is.
        """
        if self.calculator.n_sequences == 0:
            # Avoid "zero division": No disccount.
            return 1
        multiplier = 1 / self.calculator.n_sequences
        return self.calculator._default_factor(multiplier)
