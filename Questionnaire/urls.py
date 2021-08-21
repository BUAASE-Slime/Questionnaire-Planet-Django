from django.conf.urls.static import static
from django.urls import path
from Questionnaire.views import *


urlpatterns = [
    path('get_list', get_list),
]