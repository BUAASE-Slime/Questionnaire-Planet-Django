from django.urls import path
from .views import *

urlpatterns = [
    path('create_qn', create_qn_epidemic)
]