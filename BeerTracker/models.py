from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length=100)
    party_date = models.DateTimeField('Date of the party')
    party_end = models.DateTimeField('Date of the party termination')


class Drinker(User):
    pass


class Drink(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=16)
    alcohol_amount = models.DecimalField('Amount of alcohol in % ')


class StringDrink(Drink):
    pass


class SoftDrink(Drink):
    pass


class Beer(Drink):
    pass