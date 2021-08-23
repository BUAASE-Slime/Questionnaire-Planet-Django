from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [

    path('delete/qn/recover',recover_survey_from_delete),
    path('delete/qn/not_real',delete_survey_not_real),
    path('delete/qn/real',delete_survey_real),
    path('delete/qn/empty',empty_the_recycle_bin),
    path('delete/question',delete_question),
    path('delete/option',delete_option),

    path('delete/all_submit',empty_qn_all_Submit),

    path('get/qn_detail',get_survey_details),


    path('create/qn',create_qn),
    path('create/question',create_question),

    path('save/qn',save_qn),
    path('deploy_qn',deploy_qn),
    path('pause_qn',pause_qn),

    path('export/docx',TestDocument),
    path('export/pdf',pdf_document),
    path('duplicate/qn',duplicate_qn)


]
