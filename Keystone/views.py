from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.template import loader

from Keystone.forms import SignupForm


def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = authenticate(
                username=user_form.cleaned_data.get('username'),
                password=user_form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        user_form = SignupForm()
        return render(request, 'Keystone/signup.html', {
            'user_form': user_form})


def index(request):
    template = loader.get_template('../templates/Keystone/indexpage.html')
    return HttpResponse(template.render())


@login_required()
def settings(request):
    return HttpResponse("WIP")
