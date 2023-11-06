
from django.urls import path
from website.views import *
from django.urls import re_path


app_name = 'website'

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('elements', elements, name='elements'),
    path('newsletter', newsletter, name='newsletter'),
]
