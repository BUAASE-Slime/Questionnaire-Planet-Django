from django.urls import path
from .views import *

urlpatterns = [
    path('create_qn', create_qn_signup),
    path('save_qn', save_qn),
]