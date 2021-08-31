# Create your views here.
import json
import time


import datetime


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.models import *


from Submit.views import get_qn_data


@csrf_exempt
def save_exam_answer_by_code(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        code = req['code']
        answer_list = req['answers']
        username = request.session.get('username')
        if username is None or username == '':
            # username = ''
            response = {'status_code': 4, 'message': '您尚未登陆'}
            return JsonResponse(response)

        survey = Survey.objects.get(share_url=code)

        if survey.finished_time is not None and datetime.datetime.now() > survey.finished_time:
            response = {'status_code': 5, 'message': '考试已结束，不允许提交'}
            return JsonResponse(response)

        survey.recycling_num += 1
        survey.save()
        submit = Submit(username=username, survey_id=survey,score=0)
        submit.save()
        all_score = 0
        for answer_dict in answer_list:
            question = Question.objects.get(question_id=answer_dict['question_id'])
            answer = Answer(answer=answer_dict['answer'],username=username,
                            type = answer_dict['type'],question_id=question,submit_id=submit,
                            )
            answer.save()
            if answer_dict['answer'] == question.right_answer:
                answer.score = question.point
            else:
                answer.score = 0
            answer.save()

            all_score += answer.score
        submit.score = all_score
        submit.save()

        response['questions'] = get_qn_data(survey.survey_id)['questions']
        response['answers'] = req['answers']
        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)
