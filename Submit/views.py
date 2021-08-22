import json

from django.shortcuts import render
import pytz

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi

import datetime
from Qn.form import *
from Qn.models import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CollectForm

utc = pytz.UTC


# Create your views here.

@csrf_exempt
def empty_the_recycle_bin(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        username_form = UserNameForm(request.POST)
        if username_form.is_valid():
            username = username_form.cleaned_data.get('username')
            qn_list = Survey.objects.filter(username=username, is_deleted=True)
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
            response = {'status_code': -1, 'message': 'invalid form'}
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
            response['description'] = survey.description
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
                temp['must'] = item.is_must_answer
                temp['type'] = item.type
                temp['qn_id'] = id
                temp['sequence'] = item.sequence
                temp['id'] = item.sequence  # 按照前端的题目顺序
                temp['option'] = []
                if temp['type'] in ['radio', 'checkbox']:
                    # 单选题或者多选题有选项
                    option_list = Option.objects.filter(question_id=item.question_id)
                    for option_item in option_list:
                        option_dict = {}
                        option_dict['option_id'] = option_item.option_id
                        option_dict['title'] = option_item.content
                        temp['option'].append(option_dict)
                    temp['answer'] = ''
                else:  # TODO 填空题或者其他
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


# username title description type
@csrf_exempt
def create_qn(request):
    global survey
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        new_qn_form = CreateNewQnForm(request.POST)
        if new_qn_form.is_valid():
            username = new_qn_form.cleaned_data.get('username')
            title = new_qn_form.cleaned_data.get('title')
            description = new_qn_form.cleaned_data.get('description')
            type = new_qn_form.cleaned_data.get('type')

            description = "这里是问卷说明信息，您可以在此处编写关于本问卷的简介，帮助填写者了解这份问卷。"

            try:
                user = User.objects.get(username=username)

            except:
                response = {'status_code': 2, 'message': '用户不存在'}
                return JsonResponse(response)

            if request.session.get('username') != username:
                return JsonResponse({'status_code': 2})

            if title == '':
                title = "默认标题"

            try:
                survey = Survey(username=username, title=title, type=type, description=description, question_num=0,
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
def create_option(question, content, sequence):
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
    # TODO 完善json。dump
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        new_question_form = CreateNewQuestionForm(request.POST)
        if new_question_form.is_valid():
            question = Question()
            try:
                question.title = new_question_form.cleaned_data.get('title')
                question.direction = new_question_form.cleaned_data.get('direction')
                question.is_must_answer = new_question_form.cleaned_data.get('must')
                question.type = new_question_form.cleaned_data.get('type')
                survey_id = new_question_form.cleaned_data.get('qn_id')
                question.survey_id = Survey.objects.get(survey_id=survey_id)
                question.raw = new_question_form.cleaned_data.get('raw')
                question.score = new_question_form.cleaned_data.get('score')

                option_str = new_question_form.cleaned_data.get('options')
            except:
                response = {'status_code': -3, 'message': '后端炸了'}
                return JsonResponse(response)
            KEY = "^_^_^"
            option_list = option_str.split(KEY)
            for item in option_list:
                create_option(question, item)
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
def save_qn(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        print(req)
        qn_id = req['qn_id']
        try:
            question_list = Question.objects.filter(survey_id=qn_id)
        except:
            response = {'status_code': 3, 'message': '问卷不存在'}
            return JsonResponse(response)
        for question in question_list:
            question.delete()

        survey = Survey.objects.get(survey_id=qn_id)
        survey.username = req['username']
        survey.title = req['title']
        survey.description = req['description']
        survey.type = req['type']
        question_list = req['questions']

        if request.session.get("username") != req['username']:
            request.session.flush()
            return JsonResponse({'status_code': 0})

        # TODO

        for question in question_list:
            question['direction'] = ''
            create_question_in_save(question['title'], question['direction'], question['must']
                                    , question['type'], qn_id=req['qn_id'], raw=question['row'],
                                    score=question['score'],
                                    options=question['options']
                                    )

        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}


def create_question_in_save(title, direction, must, type, qn_id, raw, score, options):
    question = Question()
    try:
        question.title = title
        question.direction = direction
        question.is_must_answer = must
        question.type = type
        survey_id = qn_id
        question.survey_id = Survey.objects.get(survey_id=survey_id)
        question.raw = raw
        question.score = score
    except:
        response = {'status_code': -3, 'message': '后端炸了'}
        return JsonResponse(response)
    KEY = "^_^_^"

    option_list = options
    for item in option_list:
        print(item)
        content = item['title']
        sequence = item['id']
        create_option(question, content, sequence)
    question.save()


@csrf_exempt
def deploy_qn(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': 2, 'message': '问卷不存在'}
                return JsonResponse(response)
            if survey.is_deleted == True:
                response = {'status_code': 4, 'message': '问卷已经放入回收站'}
                return JsonResponse(response)

            if survey.is_released == True:
                response = {'status_code': 3, 'message': '问卷已经发布，不要重复操作'}
                return JsonResponse(response)

            survey.is_released = True
            if survey.release_time == '' or survey.release_time is None or survey.release_time == 'null':
                survey.release_time = datetime.datetime.now()
            survey.save()
            return JsonResponse(response)

        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def pause_qn(request):
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
                response = {'status_code': 2, 'message': '问卷已放入回收站'}
                return JsonResponse(response)
            if not survey.is_released:
                response = {'status_code': 3, 'message': '问卷为发行，不可取消发行'}
                return JsonResponse(response)
            survey.is_released = False
            survey.save()
            return JsonResponse(response)

        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)
