from django.shortcuts import render
import json

import pytz
import datetime

# Create your views here.
from utils.toHash import hash_code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Qn.form import SurveyIdForm
from Qn.form import CollectForm
from Qn.models import *

utc = pytz.UTC

@csrf_exempt
def save_qn_vote(request):
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
            question_list = Question.objects.filter(survey_id=qn,isVote=True)
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
                        'title':option.content,
                        'id':option.content,
                        'num':num
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
