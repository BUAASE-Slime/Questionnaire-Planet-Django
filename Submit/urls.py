from django.conf.urls.static import static
from django.urls import path
from .views import *
# from .no_use_func import *
from exam.views import  save_exam_answer_by_code
from vote.views import *
# from .schedules import timing_task
urlpatterns = [
    path('delete/qn/recover', recover_survey_from_delete),
    #问卷从回收站恢复
    path('delete/qn/not_real',delete_survey_not_real),
    # 问卷放入回收站
    path('delete/qn/real',delete_survey_real),
    # 彻底删除问卷
    path('delete/qn/empty',empty_the_recycle_bin),
    # 清空回收站
    # path('delete/question',delete_question),
    #单一删除问题
    # path('delete/option',delete_option),
    # 单一删除选项

    path('delete/all_submit',empty_qn_all_Submit),
    # 清空回收站

    path('get/qn_detail',get_survey_details),
    #获取问卷全部信息，
    path('get/qn_for_fill', get_survey_details_by_others),
#获取问卷全部信息但是仅供答卷填写
    path('create/qn',create_qn),
    #创建问卷

    #保存问卷但删除问题
    path('save/qn_keep/history',save_qn_keep_history),
    #保存问卷
    path('save/qn/deploy',save_and_deploy),
    #保存并发布
    # path('save/exam/paper',save_exam_answer),
    path('save/exam/paper/by/code', save_exam_answer_by_code),
    #保存考试答卷
    path('deploy_qn',deploy_qn),
    #发布问卷
    path('pause_qn',pause_qn),
    #暂停问卷
    path('export/docx',create_docx),
    #导出word
    path('export/pdf',pdf_document),
    #导出pdf
    path('export/excel',export_excel),
    #导出结果excel
    path('duplicate/qn',duplicate_qn),
    #复制问卷
    path('get/recycling_num',get_qn_recycling_num),
    #获取近期回收数目
    path('get/submit_answers',get_answer_from_submit),
    path('get/submit_answers/code', get_answer_from_submit_by_code),
    #预览答卷？
    path('delete/submit',delete_submit),
    #删除特定提交
    path('get/qn/all_submit',get_qn_all_submit),
    #获取问卷的全部提交
    path('cross/analysis',cross_analysis),
    #交叉分析
    path('get/qn/question/analysis',get_qn_question),
    #对问卷中特定问题分析的
    path('get/qn/stat_analysis',submit_reporter),
    #查看答卷
    # path('get/vote/current_situation',ret_vote_answer),
    path('get/vote/current_situation/from/code', ret_vote_answer_by_code),
    #获取投票当前结果
    path('get/ip', get_ip),
    #获取IP地址定位
    # path('get/exam/rank', get_exam_rank),

]
