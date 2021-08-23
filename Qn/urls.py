from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [

    path('get_list', get_list),
    path('get_recycling_num', get_recycling_num),
    path('get_recycling_num_total', get_recycling_num_total),
    path('get_answer', get_answer),
    path('collect', collect),
    path('not_collect', not_collect),
    path('get_code', get_code),
    path('get_code_existed', get_code_existed),
    path('get_survey_from_url', get_survey_from_url),
    path('get_ans', get_question_answer),
    path('save_ans', save_qn_answer),
]
