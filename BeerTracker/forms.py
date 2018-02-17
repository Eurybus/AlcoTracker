from django import forms

from BeerTracker.models import AlcoholConsumptionEvent, Patron


class UserDrinkEventInputForm(forms.ModelForm):
    class Meta:
        model = AlcoholConsumptionEvent
        fields = ['drink']


class PatronModificationForm(forms.ModelForm):
    class Meta:
        model = Patron
        fields = ['current_event']
