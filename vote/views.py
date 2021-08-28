from django.shortcuts import render
import json

import pytz
import datetime

# Create your views here.
from utils.toHash import hash_code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Qn.form import SurveyIdForm, URLForm, CodeForm
from Qn.models import *

utc = pytz.UTC




@csrf_exempt
def ret_vote_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                qn = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': -1, 'message': '问卷不存在'}
                return JsonResponse(response)

            # username = request.session.get('username')
            # if survey.username != username:
            #     return JsonResponse({'status_code': 0})
            question_list = Question.objects.filter(survey_id=qn, isVote=True)
            questions = []
            for question in question_list:
                item = {}
                item['question_id'] = question.question_id
                item['id'] = question.sequence
                item['description'] = question.direction
                item['isVote'] = True
                item['must'] = question.is_must_answer
                item['title'] = question.title
                item['type'] = question.type
                item['row'] = question.raw
                item['score'] = question.score
                option_list = Option.objects.filter(question_id=question)
                max_num = 0
                options = []
                answer_list = Answer.objects.filter(question_id=question)
                for option in option_list:
                    num = 0
                    for answer in answer_list:
                        if answer.answer.find(option.content) >= 0:
                            num += 1
                    if num > max_num:
                        max_num = num
                    dict = {
                        'title': option.content,
                        'id': option.content,
                        'num': num
                    }
                    options.append(dict)

                item['options'] = options
                questions.append(item)

            response['questions'] = questions

            return JsonResponse(response)
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def ret_vote_answer_by_code(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = CodeForm(request.POST)
        if survey_form.is_valid():
            code = survey_form.cleaned_data.get('code')
            try:
                qn = Survey.objects.get(share_url=code)
            except:
                response = {'status_code': 2, 'message': '问卷不存在'}
                return JsonResponse(response)

            if qn.is_released is False or qn.is_deleted is True:
                return JsonResponse({'status_code': 3})

            # username = request.session.get('username')
            # if survey.username != username:
            #     return JsonResponse({'status_code': 0})
            question_list = Question.objects.filter(survey_id=qn, isVote=True)
            questions = []
            for question in question_list:
                item = {}
                item['question_id'] = question.question_id
                item['id'] = question.sequence
                item['description'] = question.direction
                item['isVote'] = True
                item['must'] = question.is_must_answer
                item['title'] = question.title
                item['type'] = question.type
                item['row'] = question.raw
                item['score'] = question.score
                option_list = Option.objects.filter(question_id=question)
                max_num = 0
                options = []
                answer_list = Answer.objects.filter(question_id=question)
                for option in option_list:
                    num = 0
                    for answer in answer_list:
                        if answer.answer.find(option.content) >= 0:
                            num += 1
                    if num > max_num:
                        max_num = num
                    dict = {
                        'title': option.content,
                        'id': option.content,
                        'num': num
                    }
                    options.append(dict)

                item['options'] = options
                item['max_num'] = max_num
                questions.append(item)

            response['questions'] = questions

            return JsonResponse(response)
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)

    else:
        print("请求并非 POST 类型")
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)
