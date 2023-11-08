from django.urls import path
from .views import *

app_name = 'portfolio'

urlpatterns = [
    path('',portfolio, name='index'),
    path('details/',portfolio, name='details'),
]