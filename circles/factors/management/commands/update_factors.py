import os
import random
import datetime

from django.core.management.base import BaseCommand

from factors.models import FactorFunction
from factors.factory import FactorFunctionsFactory
from factors.utils import valid_factor_name


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _update_create_factor(self, factor_name):
        try:
            factor = FactorFunction.objects.get(function_name=factor_name)
            print("Factor <%s> already registered in db" % factor_name)
        except:
            print("Factor <%s> not registered in db. Adding it." % factor_name)
            factor = FactorFunction.objects.create(function_name=factor_name)

    def _update_factors(self):
        """
        Update Factor table according the functions registered in FactorFunctionsFactory.
        """
        factors_names = [
            factor_name
            for factor_name in dir(FactorFunctionsFactory) if valid_factor_name(factor_name)
        ]
        print("Checking ", factors_names)
        for factor_name in factors_names:
            self._update_create_factor(factor_name)
        print("SUCESS: Factors have been updated")

    def handle(self, *args, **options):
        self._update_factors()
