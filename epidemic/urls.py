from django.urls import path
from .views import *

urlpatterns = [

    path('save_ans_by_code', save_epidemic_answer_by_code),

    path('test', test)
]
