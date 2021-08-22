from itertools import groupby
from operator import itemgetter

import pytz
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
from django.shortcuts import render
import datetime

# Create your views here.
from .form import *
from .models import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CollectForm
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
polygon_view_get_resp = {200: '查询成功', 401: '未登录', 402: '查询失败', 403: '用户名不匹配,没有查询权限', 404: '表单不匹配'}


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='查询问卷列表',
                     operation_description=polygon_view_get_desc,
                     manual_parameters=polygon_view_get_parm,
                     responses=polygon_view_get_resp
                     )
@api_view(['POST'])
def get_list(request):
    # 检验是否登录
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        survey_id = request.POST.get('survey_id')
        is_deleted = bool(request.POST.get('is_deleted'))
        title_key = request.POST.get('title_key')
        username = request.POST.get('username')
        is_released = request.POST.get('is_released')
        is_collected = bool(request.POST.get('is_collected'))
        order_item = request.POST.get('order_item')
        order_type = request.POST.get('order_type')
        print(is_released, order_item, order_type, title_key, username, is_collected)
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
        if is_released == 1:
            survey_list = survey_list.filter(is_released=is_released)
        if is_released == 0:
            print(1)
            survey_list = survey_list.filter(is_released != is_released)
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

        if json_list:
            return JsonResponse(list(json_list), safe=False, json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'status_code': 404})



class _Params:
    USERNAME = openapi.Parameter('username', openapi.TYPE_STRING, description='用户名', type=openapi.TYPE_STRING)
    QN_ID = openapi.Parameter('qn_id', openapi.TYPE_NUMBER,description="问卷id",type=openapi.TYPE_NUMBER)

@csrf_exempt
def empty_the_recycle_bin(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        username_form = UserNameForm(request.POST)
        if username_form.is_valid():
            username = username_form.cleaned_data.get('username')
            qn_list = Survey.objects.filter(username=username,is_deleted=True)
            for qn in qn_list:
                qn.delete()
            return JsonResponse(response)
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

@csrf_exempt
def all_submittion_count(request):
    if request.method == 'POST':
        try:
            count = int(Submit.objects.all().count())
        except :
            return JsonResponse({'status_code': 1,'message':"后端炸了"})
        return JsonResponse({'status_code': 1, 'count': count,'message':"success"})
    else:
        return JsonResponse({'status_code': 0, 'count': 0,'message':"请求错误"})

@csrf_exempt
def delete_survey_not_real(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': -1, 'message': '问卷不存在'}
                return JsonResponse(response)
            if survey.is_deleted == True:
                response = {'status_code': 0, 'message': '问卷已放入回收站'}
                return JsonResponse(response)
            survey.is_deleted = True
            survey.is_released = False
            survey.save()
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)
@csrf_exempt
def delete_survey_real(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': -1, 'message': '问卷不存在'}
                return JsonResponse(response)
            survey.delete()
            # 是否真的删掉呢
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def get_survey_details(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': -2, 'message': '问卷不存在'}
                return JsonResponse(response)

            response['title'] = survey.title
            response['subtitle'] = survey.subtitle
            response['type'] = survey.type
            response['question_num'] = survey.question_num
            response['created_time'] = survey.created_time
            response['is_released'] = survey.is_released
            response['release_time'] = survey.release_time
            response['finished_time'] = survey.finished_time
            response['recycling_num'] = survey.recycling_num

            question_list = Question.objects.filter(survey_id=id)
            questions = []
            for item in question_list:
                temp = {}
                temp['question_id'] = item.question_id
                temp['title'] = item.title
                temp['direction'] = item.direction
                temp['is_must_answer'] = item.is_must_answer
                temp['type'] = item.type
                temp['qn_id'] = id
                temp['sequence'] = item.sequence
                temp['option'] = []
                if temp['type'] < 2:
                # 单选题或者多选题有选项
                    option_list = Option.objects.filter(question_id=item.question_id)
                    for option_item in option_list:
                        option_dict = {}
                        option_dict['option_id'] = option_item.option_id
                        option_dict['content'] = option_item.content
                        temp['option'].append(option_dict)
                    temp['answer']  = ''
                else:# TODO 填空题或者其他
                    pass

                questions.append(temp)
                print(questions)
            response['questions'] = questions

            return JsonResponse(response)


        else:
            response = {'status_code': -1, 'message': '问卷id不为整数'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

@csrf_exempt
def delete_question(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        question_form = QuestionIdForm(request.POST)
        if question_form.is_valid():
            id = question_form.cleaned_data.get('question_id')
            try:
                question = Question.objects.get(question_id=id)
            except:
                response = {'status_code': -1, 'message': '题目不存在'}
                return JsonResponse(response)
            question.delete()
            # 是否真的删掉呢
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

@csrf_exempt
def delete_option(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        option_form = OptionIdForm(request.POST)
        if option_form.is_valid():
            id = option_form.cleaned_data.get('option_id')
            try:
                option = Option.objects.get(option_id=id)
            except:
                response = {'status_code': -1, 'message': '选项不存在'}
                return JsonResponse(response)
            option.delete()
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

# username title subtitle type
@csrf_exempt
def create_qn(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        new_qn_form = CreateNewQnForm(request.POST)
        if new_qn_form.is_valid():
            username = new_qn_form.cleaned_data.get('username')
            title = new_qn_form.cleaned_data.get('title')
            subtitle = new_qn_form.cleaned_data.get('subtitle')
            type = new_qn_form.cleaned_data.get('type')

            try:
                user = User.objects.get(username=username)

            except:
                response = {'status_code': 2, 'message': '用户不存在'}
                return JsonResponse(response)
            # survey.username = username
            # survey.title = title
            # survey.type = int(type)
            # survey.subtitle = subtitle
            # survey.question_num = 0
            # survey.recycling_num = 0

            try:
                survey = Survey(username=username, title=title, type=type, subtitle=subtitle, question_num=0,
                                recycling_num=0)
                survey.save()
            except:
                response = {'status_code': -3, 'message': '后端炸了'}
                return JsonResponse(response)

            response['qn_id'] = survey.survey_id
            return JsonResponse(response)


        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)

@csrf_exempt
def create_option(question,content):
    option = Option()
    option.content = content
    question.option_num += 1
    option.question_id = question
    question.save()
    option.order = question.option_num
    option.save()

#  title direction is_must_answer type qn_id options:只传option的title字符串使用特殊字符例如 ^%之类的隔开便于传输
@csrf_exempt
def create_question(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        new_question_form = CreateNewQuestionForm(request.POST)
        if new_question_form.is_valid():
            question = Question()
            try:
                question.title = new_question_form.cleaned_data.get('title')
                question.direction = new_question_form.cleaned_data.get('direction')
                question.is_must_answer = new_question_form.cleaned_data.get('is_must_answer')
                question.type = new_question_form.cleaned_data.get('type')
                survey_id = new_question_form.cleaned_data.get('qn_id')
                question.survey_id = Survey.objects.get(survey_id=survey_id)

                option_str = new_question_form.cleaned_data.get('options')
            except:
                response = {'status_code': -3, 'message': '后端炸了'}
                return JsonResponse(response)
            KEY = "^_^_^"
            option_list = option_str.split(KEY)
            for item in option_list:
                create_option(question,item)
            question.save()
            response['option_num'] = len(option_list)

            return JsonResponse(response)

        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)





@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='统计问卷回收量',
                     operation_description="返回每日的问卷回收量",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True), ],
                     responses=polygon_view_get_resp
                     )
@api_view(['POST'])
def get_recycling_num(request):
    # 检验是否登录
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except:
            return JsonResponse({'status_code': 402})

        # 检查用户名是否匹配
        if survey.username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        submit_list = Submit.objects.filter(survey_id_id=survey_id)
        submit_list = submit_list.order_by('submit_time')
        json_list = []
        for submit in submit_list:
            submit.submit_time = submit.submit_time.strftime("%d")
        date = submit_list[0].submit_time
        num = 0
        for submit in submit_list:
            if submit.submit_time == date:
                num = num + 1
            else:
                json_item = {"date":date,"number":num}
                json_list.append(json_item)
                date = submit.submit_time
                num = 1

        json_item = {"date": date, "number": num}
        json_list.append(json_item)
        data = {'data': json_list}
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
@swagger_auto_schema(method='get',
                     tags=['问卷相关'],
                     operation_summary='查询全部答卷',
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


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='问卷收藏',
                     operation_description="收藏问卷",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '收藏成功', 401: '未登录', 402: '收藏失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
def collect(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except:
            return JsonResponse({'status_code': 402})

        # 检查用户名是否匹配
        if survey.username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        try:
            survey.is_collected = True
            survey.save()
            return JsonResponse({'status_code': 200})
        except:
            return JsonResponse({'status_code': 402})
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='取消收藏',
                     operation_description="取消收藏",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
def not_collect(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except:
            return JsonResponse({'status_code': 402})

        # 检查用户名是否匹配
        if survey.username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        try:
            survey.is_collected = False
            survey.save()
            return JsonResponse({'status_code': 200})
        except:
            return JsonResponse({'status_code': 402})
    else:
        return JsonResponse({'status_code': 404})
