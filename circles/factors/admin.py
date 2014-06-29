from django.contrib import admin
from factors.models import FactorFunction

# TODO: Set the ModelAdmin as a read-only model. Or maybe just not register it?
admin.site.register(FactorFunction)
