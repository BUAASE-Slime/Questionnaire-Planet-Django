from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [

    path('get_list', get_list),
    path('get_recycling_num', get_recycling_num),
    path('get_answer', get_answer),
    path('collect', collect),
    path('not_collect', not_collect),


]
