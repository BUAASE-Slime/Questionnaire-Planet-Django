from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [

    path('delete/qn/',delete_survey),
    path('delete/question/',delete_question),
]
