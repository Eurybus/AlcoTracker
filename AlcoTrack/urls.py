"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from rest import views as rviews
from BeerTracker import views as bviews
from Keystone import  views as keystone_views

router = routers.DefaultRouter()
router.register(r'users', rviews.UserViewSet)
router.register(r'groups', rviews.GroupViewSet)

urlpatterns = [
    path('', bviews.HomeView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('logalco/', login_required(bviews.InputDrinkEvent.as_view()),
         name='log-drink'),
    path('events/', login_required(bviews.EventListView.as_view()),
         name='event-list'),
    path('events/<int:pk>', login_required(bviews.EventDetailView.as_view()),
         name='event-detail'),
    path('home/', bviews.HomeView.as_view(), name='home'),
    #url(r'^api/', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/$|^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^registration/$', keystone_views.signup, name='registration'),
    url(r'^settings/$',
        login_required(bviews.PatronModificationView.as_view()),
        name='settings'),


]
