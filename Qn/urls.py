from django.conf.urls.static import static
from django.urls import path
from Qn.views import *


urlpatterns = [
    path('get_list', get_list),
    path('get_recycling_num', get_recycling_num),
]