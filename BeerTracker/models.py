from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    description = models.TextField(null=True)

    def __str__(self):
        return "{} at {}, from {}".format(
            self.name, self.venue, self.party_date)

    @property
    def is_ongoing(self):
        current_time = now()
        return True if current_time.time() < self.party_end.time() else False

    @property
    def current_patrons(self):
        return self.patrons.all()

    @property
    def drink_events(self):
        return (
            AlcoholConsumptionEvent.objects.
                filter(event_id=self.pk).order_by('timestamp').reverse()
        )

    @property
    def drink_events_hard(self):
        return self.drink_events.filter(
            drink__type__drink_class__in=[3, 4, 5])

    @property
    def drink_events_soft(self):
        return self.drink_events.filter(
            drink__type__drink_class__in=[1, 2])


class Patron(models.Model):
    """
    Links to User model. Used to keep track of application specific things.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_event = models.ForeignKey(Event, null=True, blank=True,
                                      related_name="patrons",
                                      on_delete=models.CASCADE)

    @property
    def full_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.full_name


class DrinkType(models.Model):

    DRINK_CLASSES = (
        (0, 'Alcohol free - ~0%'),
        (1, 'Soft alcholic beverage - <9%'),
        (2, 'Strong alcoholic beverage - 9%-22%'),
        (3, 'Liquor - 20%-50%'),
        (4, 'Strong liquor - >50%'),
        (5, 'Mixed drink - Any ABV'),
    )
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
        return "{}: {}% {}ml".format(
            self.name, self.alcohol_amount, self.liquid_amount)


class AlcoholConsumptionEvent(models.Model):
    """
    This model is used to keep track of each persons' consumed alcohol
    """
    drinker = models.ForeignKey(Patron, on_delete=models.CASCADE,
                                related_name='consumptions')
    timestamp = models.DateTimeField(default=now)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return "{} drank {} on {} at {}".format(
            self.drinker, self.drink.name, self.timestamp.time(),
            self.event.name)

    @property
    def drinker_name(self):
        return self.drinker.user.first_name


class LiveSetting(models.Model):
    """
    Used to store settings which are not hardcoded
    """

    current_default_event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        help_text='Sets current event to new accounts')


# Signal listeners
@receiver(post_save, sender=User)
def create_user_patron(sender, instance, created, **kwargs):
    if created:
        Patron.objects.create(user=instance)
        if LiveSetting.objects.first() is not None:
            instance.patron.current_event = \
                LiveSetting.objects.first().current_default_event


@receiver(post_save, sender=User)
def save_user_patron(sender, instance, **kwargs):
    if instance.username != 'admin':
        instance.patron.save()
