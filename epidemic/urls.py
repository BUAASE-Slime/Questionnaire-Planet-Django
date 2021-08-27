from django.urls import path
from .views import *

urlpatterns = [
    path('create_qn', create_qn_epidemic),
    path('save_ans', save_epidemic_answer),
    path('upload_img',upload_image),
]