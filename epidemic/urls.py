from django.urls import path
from .views import *

urlpatterns = [
    # path('create_qn', create_qn_epidemic),
    path('save_ans', save_epidemic_answer),
    path('save_ans_by_code', save_epidemic_answer_by_code),
    # path('upload_img', upload_image),
    # path('get_img', get_image_url),
    # path('upload_video', upload_video),
    # path('get_video', get_video_url),
    # path('test', test)
]
