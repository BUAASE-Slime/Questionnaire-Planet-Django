from django.shortcuts import render
import json

import pytz
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
import datetime

# Create your views here.
from Submit.views import produce_time
from utils.toHash import hash_code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CollectForm, CreateNewQnForm, SurveyIdForm
from Qn.models import *

utc = pytz.UTC


# Create your views here.

def change_signup_max(request):
    response = {'status_code': 1, 'message': 'success'}

    if request.method == 'POST':
        req = json.loads(request.body)
        # print(req)
        qn_id = req['qn_id']
        try:
            max_num = int(req['max_num'])
        except:
            response = {'status_code': 3, 'message': '未传输最大回收数目'}
            return JsonResponse(response)

        survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
        survey.max_recycling = max_num
        survey.save()
        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)


@csrf_exempt
def save_ans_signup(request):
    response = {'status_code': 1, 'message': 'success'}
    username = request.session.get('username')
    if request.method == 'POST':
        req = json.loads(request.body)
        # print(req)
        qn_id = req['qn_id']

        survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
        if survey.recycling_num >= survey.max_recycling:
            response = {'status_code': 5, 'message': '报名数已满，无法报名'}
            return JsonResponse(response)

        survey.recycling_num = survey.recycling_num + 1
        survey.save()

        submit = Submit(survey_id=survey)

        if username == '' or username is None:
            response = {'status_code': 4, 'message': '报名需要用户登录，请登录'}
            return JsonResponse(response)

        if username:
            submit.username = username
        submit.save()

        answer_list = req['answers']
        for item in answer_list:
            answer = Answer(question_id_id=item['question_id'], submit_id_id=submit.submit_id,
                            answer=item['answer'], type=item['type'])
            if username:
                answer.username = username
            answer.save()

        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)


# username title description type
@csrf_exempt
def create_qn_signup(request):
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
            if type == '2':
                description = "这里是考试问卷说明信息，您可以在此处编写关于本考试问卷的简介，帮助填写者了解这份问卷。"
            if type == '4':
                description = "这里是报名问卷说明信息，您可以在此处编写关于本考试问卷的简介，帮助填写者了解这份问卷。"
            try:
                user = User.objects.get(username=username)

            except:
                response = {'status_code': 2, 'message': '用户不存在'}
                return JsonResponse(response)

            if request.session.get('username') != username:
                return JsonResponse({'status_code': 2})

            if title == '':
                title = "默认标题"
                if type == '2':
                    title = "默认标题"

            try:
                survey = Survey(username=username, title=title, type=type, description=description, question_num=0,
                                recycling_num=0)
                survey.save()
            except:
                response = {'status_code': -3, 'message': '后端炸了'}
                return JsonResponse(response)

            # 报名问卷问题模板
            if type == '4':
                questions = [{"id": 1, "type": "text", "title": "你的姓名是：",
                              "must": True, "description": '', "row": 1, "score": 0, "options": [{'id': 1, 'title': ""}]},
                             {"id": 2, "type": "text", "title": "你的手机号是：",
                              "must": True, "description": '', "row": 1, "score": 0, "options": [{'id': 1, 'title': ""}]}]

                options = [{"hasNumLimit": True, "title": "班长", "id": 1, "supply": 10, "remain": 10},
                           {"hasNumLimit": True, "title": "团支书", "id": 2, "supply": 10, "remain": 10},
                           {"hasNumLimit": True, "title": "学习委员", "id": 3, "supply": 10, "remain": 10}]

                questions.append({"id": 3, "type": "radio", "title": "您想要竞选的职位是：",
                                  "must": True, "description": '', "row": 1, "score": 0, "options": options})
                response['questions'] = questions

            response['qn_id'] = survey.survey_id
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
            survey = Survey.objects.get(survey_id=qn_id)
        except:
            response = {'status_code': 3, 'message': '问卷不存在'}
            return JsonResponse(response)
        submit_list = Submit.objects.filter(survey_id=qn_id)
        for submit in submit_list:
            submit.is_valid = False
            submit.save()

        questions = Question.objects.filter(survey_id=survey)

        survey.username = req['username']
        survey.title = req['title']
        if survey.title == '':
            survey.title = "默认标题"
        survey.description = req['description']
        if survey.description == '':
            survey.description = "这里是问卷说明信息，您可以在此处编写关于本问卷的简介，帮助填写者了解这份问卷。"
        survey.type = req['type']

        survey.save()
        question_list = req['questions']

        if request.session.get("username") != req['username']:
            request.session.flush()
            return JsonResponse({'status_code': 0})

        # 报名问卷
        if req['type'] == '4':
            survey.max_recycling = req['max_recycling']
            survey.save()

        for question in questions:
            num = 0
            for question_dict in question_list:
                if question_dict['question_id'] == question.question_id:
                    # 旧问题在新问题中有 更新问题
                    question_dict_to_question(question, question_dict)
                    num = 1
                    break

            if num == 0:
                question.delete()

        for question_dict in question_list:
            try:
                question_dict['question_id'] = question_dict['question_id']
            except:
                question_dict['question_id'] = 0
            refer = ''
            point = 0
            if req['type'] == '2':
                refer = question_dict['refer']
                point = question_dict['point']
                print("this question point  = " + str(question_dict['point']))

            if question_dict['question_id'] == 0:
                create_question_in_save(question_dict['title'], question_dict['description'], question_dict['must']
                                        , question_dict['type'], qn_id=req['qn_id'], raw=question_dict['row'],
                                        score=question_dict['score'],
                                        options=question_dict['options'],
                                        sequence=question_dict['id'], refer="", point=0
                                        )

        question_num = 0

        survey.save()
        question_list = Question.objects.filter(survey_id=survey)
        for question in question_list:
            question_num += 1
        survey.question_num = question_num
        print("保存成功，该问卷的问题数目为：" + str(question_num))
        survey.save()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}


@csrf_exempt
def create_question_in_save(title, direction, must, type, qn_id, raw, score, options, sequence, refer, point):
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
        question.sequence = sequence
        question.point = point
        question.right_answer = refer
    except:
        response = {'status_code': -3, 'message': '后端炸了'}
        return JsonResponse(response)
    KEY = "^_^_^"

    option_list = options
    for item in option_list:
        print(item)
        content = item['title']
        sequence = item['id']
        has_num_limit = False
        num_limit = 0
        remain_num = 0
        if question.survey_id.type == '4':
            has_num_limit = item['hasNumLimit']
            num_limit = item['supply']
            remain_num = item['remain']
        create_option(question, content, sequence, has_num_limit, num_limit, remain_num)
    question.save()


@csrf_exempt
def create_option(question, content, sequence, has_num_limit, num_limit, remain_num):
    option = Option()
    option.content = content
    question.option_num += 1
    option.question_id = question
    question.save()
    option.order = sequence
    option.has_num_limit = has_num_limit
    option.num_limit = num_limit
    option.remain_num = remain_num
    option.save()


@csrf_exempt
def question_dict_to_question(question, question_dict):
    # question = Question()#TODO delete
    question.title = question_dict['title']
    print(question_dict)
    question.direction = question_dict['description']
    question.is_must_answer = question_dict['must']
    question.type = question_dict['type']
    # qn_id =  question_dict['qn_id']
    # question.survey_id = Survey.objects.get(survey_id=qn_id)
    question.raw = question_dict['row']
    question.score = question_dict['score']
    options = question_dict['options']
    question.sequence = question_dict['id']

    if question.survey_id.type == '2':
        question.right_answer = question_dict['refer']
        question.point = question_dict['point']

    option_list_delete = Option.objects.filter(question_id=question)
    for option in option_list_delete:
        option.delete()
    option_list = options
    # option_list = option_set[0]
    # print("options") ,print(options)
    print(option_list)

    for item in option_list:
        print("item", end=" ")
        print(item)
        content = item['title']
        sequence = item['id']
        has_num_limit = False
        num_limit = 0
        remain_num = 0
        if question.survey_id.type == '4':
            has_num_limit = item['hasNumLimit']
            num_limit = item['supply']
            remain_num = item['remain']
        create_option(question, content, sequence, has_num_limit, num_limit, remain_num)
    question.save()


@csrf_exempt
def get_survey_details(request):
    response = {'status_code': 1, 'message': 'success'}
    this_username = request.session.get('username')
    # if not this_username:
    #     return JsonResponse({'status_code': 0})
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                survey = Survey.objects.get(survey_id=id)
                print(survey.survey_id)
            except:
                response = {'status_code': -2, 'message': '问卷不存在'}
                return JsonResponse(response)

            # if survey.username != this_username:
            #     return JsonResponse({'status_code': 0})

            response = get_qn_data(id)

            return JsonResponse(response)
        else:
            response = {'status_code': -1, 'message': '问卷id不为整数'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


def get_qn_data(qn_id):
    id = qn_id
    survey = Survey.objects.get(survey_id=qn_id)
    response = {'status_code': 1, 'message': 'success'}
    response['qn_id'] = survey.survey_id
    response['username'] = survey.username
    response['title'] = survey.title
    response['description'] = survey.description
    response['type'] = survey.type

    response['question_num'] = survey.question_num
    response['created_time'] = response['release_time'] = response['finished_time'] = ''
    if produce_time(survey.created_time):
        response['created_time'] = survey.created_time.strftime("%Y/%m/%d %H:%M")
    if produce_time(survey.finished_time):
        response['finished_time'] = survey.finished_time.strftime("%Y/%m/%d %H:%M")
    if produce_time(survey.release_time):
        response['release_time'] = survey.release_time.strftime("%Y/%m/%d %H:%M")
    response['is_released'] = survey.is_released
    response['is_deleted'] = survey.is_deleted
    response['is_finished'] = survey.is_finished
    response['share_url'] = survey.share_url
    response['docx_url'] = survey.docx_url
    response['pdf_url'] = survey.pdf_url
    response['excel_url'] = survey.excel_url
    response['recycling_num'] = survey.recycling_num
    response['max_recycling'] = survey.max_recycling

    question_list = Question.objects.filter(survey_id__survey_id=qn_id)
    questions = []
    for item in question_list:
        temp = {}
        temp['question_id'] = item.question_id
        temp['row'] = item.raw
        temp['score'] = item.score
        temp['title'] = item.title
        temp['description'] = item.direction
        temp['must'] = item.is_must_answer
        temp['type'] = item.type
        temp['qn_id'] = qn_id
        temp['sequence'] = item.sequence
        temp['option_num'] = item.option_num
        temp['refer'] = item.right_answer
        temp['point'] = item.point
        temp['id'] = item.sequence  # 按照前端的题目顺序
        temp['options'] = [{'id': 1, 'title': ""}]
        temp['answer'] = item.right_answer
        if temp['type'] in ['radio', 'checkbox']:
            temp['options'] = []
            # 单选题或者多选题有选项
            option_list = Option.objects.filter(question_id=item.question_id)
            for option_item in option_list:
                option_dict = {}
                option_dict['id'] = option_item.option_id
                option_dict['title'] = option_item.content

                if survey.type == '4':
                    option_dict['hasNumLimit'] = option_item.has_num_limit
                    option_dict['supply'] = option_item.num_limit
                    option_dict['remain'] = option_item.remain_num

                temp['options'].append(option_dict)

        elif temp['type'] in ['mark', 'text', 'name', 'stuId', 'class', 'school']:
            pass
        elif temp['type'] == 'info':
            pass

        questions.append(temp)
        print(questions)
    response['questions'] = questions
    return response
