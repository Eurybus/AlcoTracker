from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views import View
from django.views.generic import CreateView

from BeerTracker.models import AlcoholConsumptionEvent


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


@login_required()
def home(request):
    template = loader.get_template('../templates/BeerTracker/home.html')
    return HttpResponse(template.render())


@login_required()
class EventView(View):
    def get(self, request):
        template = loader.get_template(
            '../templates/BeerTracker/beerInput.html')
        return HttpResponse(template.render())


class InputDrinkEvent(AjaxableResponseMixin, CreateView):
    model = AlcoholConsumptionEvent
    fields = ['drink']
    template_name = '../templates/BeerTracker/beerInput.html'
    success_url = '/logalco/'

    def form_valid(self, form):
        form.instance.drinker = self.request.user.patron
        form.instance.event = self.request.user.patron.current_event
        return super().form_valid(form)