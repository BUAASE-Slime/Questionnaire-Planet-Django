from django.urls import path

from exam.views import *

urlpatterns = [
    path('get_ans', get_answer),
    path('get_qn_url', get_qn_from_url),
    path('get_que_ans', get_question_answer),
    path('save_ans', save_qn_answer),
    path('set_finish', set_finish),
    path('create_question', create_question),
    path('save_qn', save_qn),
]