from django import forms

from BeerTracker.models import AlcoholConsumptionEvent


class UserDrinkEventInputForm(forms.ModelForm):
    class Meta:
        model = AlcoholConsumptionEvent
        fields = 'drink'

