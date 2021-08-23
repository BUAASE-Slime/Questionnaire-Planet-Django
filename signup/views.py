from django.shortcuts import render
import json

import pytz
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
import datetime

# Create your views here.
from utils.toHash import hash_code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CollectForm
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
def save_qn_signup(request):
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