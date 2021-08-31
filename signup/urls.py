from django.urls import path
from .views import *

urlpatterns = [
    path('save_answer_by_code', save_signup_answer_by_code),
]
