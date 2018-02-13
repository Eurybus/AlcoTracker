from django.contrib import admin
from django.contrib.admin import register

from .models import (Venue,
                     Drink,
                     DrinkType,
                     Event,
                     AlcoholConsumptionEvent,
                     Patron,
                     LiveSetting)


@register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name']


@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'party_date']


@register(Patron)
class PatronAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name']


admin.site.register(DrinkType)
admin.site.register(Drink)
admin.site.register(AlcoholConsumptionEvent)
admin.site.register(LiveSetting)
