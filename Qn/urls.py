from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [

    path('get_list', get_list),

    path('get_answer', get_answer),
    path('collect', collect),
    path('not_collect', not_collect),
    path('get_code', get_code),
    path('get_code_existed', get_code_existed),

    path('save_ans', save_qn_answer),

    path('change/code',change_code),
]
