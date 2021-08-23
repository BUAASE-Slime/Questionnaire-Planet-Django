from django.conf.urls.static import static
from django.urls import path
from .views import *
from signup.views import *
from vote.views import *
urlpatterns = [

    path('delete/qn/recover',recover_survey_from_delete),
    path('delete/qn/not_real',delete_survey_not_real),
    path('delete/qn/real',delete_survey_real),
    path('delete/qn/empty',empty_the_recycle_bin),
    path('delete/question',delete_question),
    path('delete/option',delete_option),

    path('delete/all_submit',empty_qn_all_Submit),

    path('get/qn_detail',get_survey_details),
    path('get/qn_for_fill', get_survey_details_by_others),


    path('create/qn',create_qn),
    path('create/question',create_question),

    path('save/qn',save_qn),
    path('deploy_qn',deploy_qn),
    path('pause_qn',pause_qn),

    path('export/docx',TestDocument),
    path('export/pdf',pdf_document),
    path('export/excel',export_excel),

    path('duplicate/qn',duplicate_qn),

    path('get/vote/answer',save_qn_vote),
    path('get/signup/answer',save_qn_signup), # 提交报名问卷

    path('change/signup/max',change_signup_max),  #更改报名问卷最大报名人数


]
