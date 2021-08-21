from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [

    path('submit',all_submittion_count),

]
