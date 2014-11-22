import datetime

from django.db import models

class Color(models.Model):
    LIGHT, DARK = 0, 1
    (RED,
    YELLOW,
    BLUE,
    ORANGE,
    PURPLE,
    GREEN,
    BLACK) = range(7)

    TONALITY = (
        (LIGHT, 'Light'),
        (DARK, 'Dark'),
    )
    COLORS = (
        (RED, 'Red'),
        (YELLOW, 'Yellow'),
        (BLUE, 'Blue'),
        (ORANGE, 'Orange'),
        (PURPLE, 'Purple'),
        (GREEN, 'Green'),
        (BLACK, 'Black'),
    )
    color = models.IntegerField(max_length=2, choices=COLORS)
    tonality = models.IntegerField(max_length=1, choices=COLORS)
    hex_code = models.CharField(max_length=6, unique=True)

    def __unicode__(self):
        return self.COLORS[self.color][1]

class Sequence(models.Model):
    MAX_COLORS = 7

    players = models.ManyToManyField("Player")
    colors = models.ManyToManyField("Color")

"""
    def clean(self):
        if self.colors.count() != self.MAX_COLORS:
            raise ValidationError("You can ONLY pick %s colors" % self.MAX_COLORS)
"""


class Player(models.Model):
    paypal = models.EmailField()
    #sequences = models.ManyToManyField("Sequence")
    payments = models.ManyToManyField("Payment")
    moves = models.ManyToManyField("SequenceGame")


class Payment(models.Model):
    paypal_txn_id = models.CharField(max_length=20, unique=True)
    payment_gross = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(max_length=3)
    #sequences_number = models.IntegerField()
    sequences_shown = models.IntegerField()
    game = models.ForeignKey("Game")


class Game(models.Model):
    AVAILABLE_COLORS = 7
    MAX_DISCOUNT = 0.25

    #sequences = models.ManyToManyField("Sequence", null=True, blank=True)
    sequences = models.ManyToManyField("Sequence", null=True, blank=True, through='SequenceGame')
    initial_amount = models.IntegerField()
    percentage = models.IntegerField()
    prize = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # Payment to see a sequence
    base_payment = models.DecimalField(max_digits=8, decimal_places=2)
    winner_sequence = models.OneToOneField("Sequence", related_name="+", null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    available_colors = models.ManyToManyField("Color")
    factors = models.ManyToManyField("factors.FactorFunction", null=True, blank=True)
    max_discount = models.DecimalField(max_digits=3, decimal_places=2, default=MAX_DISCOUNT)

    def is_available(self):
        now = datetime.datetime.now()
        return (now >= self.start_date) and (now <= self.end_date)

    def __unicode__(self):
        return str(self.pk)

"""
    def clean(self):
        if self.available_colors.count() != self.AVAILABLE_COLORS:
            raise ValidationError("You have to set %s colors" % self.AVAILABLE_COLORS)
"""

class SequenceGame(models.Model):
    sequence = models.ForeignKey("Sequence")
    game = models.ForeignKey("Game")
    n_moves = models.PositiveIntegerField()
