from django.db import models


class FactorFunction(models.Model):
    function_name = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return self.function_name
