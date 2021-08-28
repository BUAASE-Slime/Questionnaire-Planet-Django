from django.conf.urls.static import static
from django.urls import path
from .views import *
from .no_use_func import *
from exam.views import save_exam_answer, save_exam_answer_by_code
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
    path('save/qn_keep/history',save_qn_keep_history),
    path('save/exam/paper',save_exam_answer),
    path('save/exam/paper/by/code', save_exam_answer_by_code),
    path('deploy_qn',deploy_qn),
    path('pause_qn',pause_qn),

    path('export/docx',TestDocument),
    path('export/pdf',pdf_document),
    path('export/excel',export_excel),

    path('duplicate/qn',duplicate_qn),

    path('get/recycling_num',get_qn_recycling_num),

    path('get/submit_answers',get_answer_from_submit),
    path('get/submit_answers/code', get_answer_from_submit_by_code),

    path('delete/submit',delete_submit),

    path('get/qn/all_submit',get_qn_all_submit),
    path('cross/analysis',cross_analysis),

    path('get/qn/question/analysis',get_qn_question),
    path('get/qn/stat_analysis',submit_reporter),

    path('get/vote/current_situation',ret_vote_answer),
    path('get/vote/current_situation/from/code', ret_vote_answer_by_code),

    path('get/ip', get_ip),
    path('get/exam/rank', get_exam_rank),
]
