from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, \
    ListView, FormView

from BeerTracker.forms import PatronModificationForm
from BeerTracker.models import AlcoholConsumptionEvent, Event, Patron


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


class HomeView(TemplateView):
    template_name = '../templates/BeerTracker/home.html'


class EventListView(ListView):
    model = Event
    template_name = "../templates/BeerTracker/event-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)


class EventDetailView(DetailView):
    template_name = "../templates/BeerTracker/event-detail.html"
    model = Event

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class InputDrinkEvent(AjaxableResponseMixin, CreateView):
    model = AlcoholConsumptionEvent
    fields = ['drink']
    template_name = '../templates/BeerTracker/beerInput.html'
    success_url = '/logalco/'

    def form_valid(self, form):
        form.instance.drinker = self.request.user.patron
        form.instance.event = self.request.user.patron.current_event
        return super().form_valid(form)


class PatronModificationView(FormView):
    form_class = PatronModificationForm
    template_name = '../templates/BeerTracker/patron-detail.html'
    success_url = reverse_lazy('settings')

    def form_valid(self, form):
        resp = super().form_valid(form)
        patron = Patron.objects.get(user=self.request.user)
        patron.current_event = form.instance.current_event
        patron.save()
        return resp


