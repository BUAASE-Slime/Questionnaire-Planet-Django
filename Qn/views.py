from itertools import groupby
from operator import itemgetter

import pytz
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import BooleanFilter
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from Qn.models import *

utc = pytz.UTC

polygon_view_get_desc = '根据所选参数,获取问卷列表,默认按创建时间倒序'
polygon_view_get_parm = [
    Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号', type=TYPE_INTEGER, required=False),
    Parameter(name='is_deleted', in_=IN_QUERY, description='是否删除', type=TYPE_BOOLEAN, required=False),
    Parameter(name='title_key', in_=IN_QUERY, description='标题关键词', type=TYPE_STRING, required=False),
    Parameter(name='username', in_=IN_QUERY, description='发起人用户名', type=TYPE_STRING, required=True),
    Parameter(name='is_released', in_=IN_QUERY, description='是否发布', type=TYPE_BOOLEAN, required=False),
    Parameter(name='is_collected', in_=IN_QUERY, description='是否收藏,', type=TYPE_BOOLEAN, required=False),
    Parameter(name='order_item', in_=IN_QUERY, description='排序项,created_time-创建时间,release_time-发布时间,recycling_num-回收量',
              type=TYPE_STRING, required=False),
    Parameter(name='order_type', in_=IN_QUERY, description='排序类型,desc-倒序,asc-正序', type=TYPE_STRING, required=False),
]
polygon_view_get_resp = {200: '查询成功', 401: '未登录', 402: '查询失败', 403: '用户名不匹配,没有查询权限'}


@csrf_exempt
@swagger_auto_schema(method='get',
                     tags=['问卷相关'],
                     operation_summary='查询问卷列表',
                     operation_description=polygon_view_get_desc,
                     manual_parameters=polygon_view_get_parm,
                     responses=polygon_view_get_resp
                     )
@api_view(['GET'])
def get_list(request):
    # 检验是否登录
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'GET':
        survey_id = request.GET.get('survey_id')
        is_deleted = bool(request.GET.get('is_deleted'))
        title_key = request.GET.get('title_key')
        username = request.GET.get('username')
        is_released = bool(request.GET.get('is_released'))
        is_collected = bool(request.GET.get('is_collected'))
        order_item = request.GET.get('order_item')
        order_type = request.GET.get('order_type')
        if order_item is None:
            order_item = "created_time"
        if order_type is None:
            order_type = "desc"

        # 用户名是否匹配
        if username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        if survey_id is not None:
            try:
                survey = Survey.objects.get(survey_id=survey_id)
                json_item = {"survey_id": survey.survey_id, "title": survey.title,
                             "subtitle": survey.subtitle, "is_released": survey.is_released,
                             "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                             "recycling_num": survey.recycling_num, "username": survey.username,
                             "created_time": survey.created_time, "release_time": survey.release_time}
                return JsonResponse(json_item)
            except:
                return JsonResponse({'status_code': 402})

        survey_list = Survey.objects.all()
        if is_deleted:
            survey_list = survey_list.filter(is_deleted=is_deleted)
        if title_key:
            survey_list = survey_list.filter(title__contains=title_key)
        if username:
            survey_list = survey_list.filter(username=username)
        if is_released:
            survey_list = survey_list.filter(is_released=is_released)
        if is_collected:
            survey_list = survey_list.filter(is_collected=is_collected)
        if order_type == 'desc':
            survey_list = survey_list.order_by('-' + order_item)
        else:
            survey_list = survey_list.order_by(order_item)

        json_list = []
        for survey in survey_list:
            json_item = {"survey_id": survey.survey_id, "title": survey.title,
                         "subtitle": survey.subtitle, "is_released": survey.is_released,
                         "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                         "recycling_num": survey.recycling_num, "username": survey.username,
                         "created_time": survey.created_time, "release_time": survey.release_time}
            json_list.append(json_item)
        return JsonResponse(list(json_list), safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@swagger_auto_schema(method='get',
                     tags=['问卷相关'],
                     operation_summary='统计问卷回收量',
                     operation_description="返回每日的问卷回收量",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True), ],
                     responses=polygon_view_get_resp
                     )
@api_view(['GET'])
def get_recycling_num(request):
    # 检验是否登录
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'GET':
        survey_id = request.GET.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except:
            return JsonResponse({'status_code': 402})

        if survey.username != request.session.get('username'):
            return JsonResponse({'status_code': 403})
        submit_list = survey.submit_set.all()
        submit_list = submit_list.order_by('submit_time')
        json_list = []
        for date, items in groupby(submit_list, key=itemgetter('submit_time')):
            number = 0
            for i in items:
                number = number + 1
            json_item = {"date": date, "number": number}
            json_list.append(json_item)
        return JsonResponse(list(json_list), safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@swagger_auto_schema(method='get',
                     tags=['问卷相关'],
                     operation_summary='返回答卷',
                     operation_description="返回用户的所有答案",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True),
                                        Parameter(name='username', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_STRING, required=True)],
                     responses=polygon_view_get_resp
                     )
@api_view(['GET'])
def get_answer(request):
    # 检验是否登录
    global answer_questions
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'GET':
        survey_id = request.GET.get('survey_id')
        username = request.GET.get('username')

        # 用户名是否匹配
        if username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        # 问卷信息
        result = {}
        try:
            survey = Survey.objects.get(survey_id=survey_id)
            if username != survey.username:
                return JsonResponse({'status_code': 403})
        except:
            return JsonResponse({'status_code': 402})
        result['survey_id'] = survey_id
        result['title'] = survey.title
        result['subtitle'] = survey.subtitle
        result['username'] = username

        # 回答信息
        result_answers = []
        questions = Question.objects.filter(survey_id=survey).order_by('sequence')
        submits = Submit.objects.filter(survey_id=survey)

        for submit in submits:
            answer_questions = []
            for question in questions:
                answer_question = {"question_id": question.id, "sequence": question.sequence,
                                   "title": question.title, "direction": question.direction,
                                   "is_must_answer": question.is_must_answer, "type": question.type}
                answer = Answer.objects.get(question_id=question, submit_id=submit)
                answer_question['answer'] = answer
                answer_questions.append(answer_question)
            result_answers.append(answer_questions)

        result['answers'] = result_answers
        return JsonResponse(result)
