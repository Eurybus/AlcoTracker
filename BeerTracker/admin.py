from django.contrib import admin
from django.contrib.admin import register

from .models import (Venue,
                     Drink,
                     DrinkType,
                     Event,
                     AlcoholConsumptionEvent,
                     Patron)


@register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name']


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'party_date']

admin.site.register(DrinkType)
admin.site.register(Drink)
admin.site.register(AlcoholConsumptionEvent)
admin.site.register(Patron)