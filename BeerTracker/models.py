from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    party_date = models.DateTimeField('Date of the party')
    party_end = models.DateTimeField('Date of the party termination')

    def __str__(self):
        return "{} at {} starting from {}".format(
            self.name, self.venue, self.party_date)

    @property
    def current_patrons(self):
        return self.patrons.all()


class Patron(models.Model):
    """
    Links to User model. Used to keep track of application specific things.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_event = models.ForeignKey(Event, null=True, blank=True,
                                      related_name="patrons",
                                      on_delete=models.CASCADE)
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=16)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name


class DrinkType(models.Model):

    DRINK_CLASSES = {
        (0, 'Alcohol free'),
        (1, 'Soft alcholic drink'),
        (2, 'Liquor'),
        (3, 'Hard liquor')

    }
    name = models.CharField(max_length=24, unique=True)
    drink_class = models.IntegerField('Drink class', choices=DRINK_CLASSES)

    def __str__(self):
        return "{}, {}".format(self.name, self.drink_class)


class Drink(models.Model):

    name = models.CharField(max_length=24, unique=True)
    type = models.ForeignKey(DrinkType, on_delete=models.CASCADE)
    alcohol_amount = models.DecimalField('Amount of alcohol in % ',
                                         null=True,
                                         blank=True,
                                         decimal_places=1,
                                         max_digits=3)
    liquid_amount = models.IntegerField('Amount of liquid (ml)')

    def __str__(self):
        return "{} ({}): {}% {}".format(
            self.name, self.type, self.alcohol_amount, self.liquid_amount)


class AlcoholConsumptionEvent(models.Model):
    """
    This model is used to keep track of each persons' consumed alcohol
    """
    drinker = models.ForeignKey(Patron, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)

    def __str__(self):
        return "{} drank {} at {}".format(
            self.drinker, self.drink.name, self.timestamp.time())
