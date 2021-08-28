# Create your views here.
import json
import time

import pytz
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
import datetime

# Create your views here.

from exam.forms import *
# from .form import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.models import *



# @csrf_exempt
# @swagger_auto_schema(method='post',
#                      tags=['问卷相关'],
#                      operation_summary='查询全部答卷',
#                      operation_description="返回用户的所有答案",
#                      manual_parameters=[Parameter(name='qn_id', in_=IN_QUERY, description='问卷编号',
#                                                   type=TYPE_INTEGER, required=True),
#                                         Parameter(name='username', in_=IN_QUERY, description='用户名',
#                                                   type=TYPE_STRING, required=True)],
#                      responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
#                      )
# @api_view(['POST'])
# def get_answer(request):
#     # 检验是否登录
#     global answer_questions
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 401})
#
#     answer_form = AnswerForm(request.POST)
#     if answer_form.is_valid():
#         qn_id = answer_form.cleaned_data.get('qn_id')
#         username = answer_form.cleaned_data.get('username')
#
#         # 用户名是否匹配
#         if username != request.session.get('username'):
#             return JsonResponse({'status_code': 403})
#
#         # 问卷信息
#         result = {}
#         try:
#             survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
#             if username != survey.username:
#                 return JsonResponse({'status_code': 403})
#         except:
#             return JsonResponse({'status_code': 402})
#         result['qn_id'] = qn_id
#         result['title'] = survey.title
#         result['description'] = survey.description
#         result['username'] = username
#
#         # 回答信息
#         result_answers = []
#         questions = Question.objects.filter(survey_id=survey).order_by('sequence')
#         submits = Submit.objects.filter(survey_id=survey)
#
#         for submit in submits:
#             answer_questions = {'sum_score': submit.score, 'question': []}
#             for question in questions:
#                 answer_question = {"question_id": question.question_id, "sequence": question.sequence,
#                                    "title": question.title, "direction": question.direction,
#                                    "is_must_answer": question.is_must_answer, "type": question.type,
#                                    'right_answer': question.right_answer}
#                 answer = Answer.objects.get(question_id=question, submit_id=submit)
#                 answer_question['answer'] = answer.answer
#                 answer_question['score'] = answer.score
#                 answer_questions['question'].append(answer_question)
#             result_answers.append(answer_questions)
#
#         result['answers'] = result_answers
#         return JsonResponse(result, safe=False)
#     else:
#         return JsonResponse({'status_code': 404})




# @csrf_exempt
# @swagger_auto_schema(method='post',
#                      tags=['问卷相关'],
#                      operation_summary='获取题目答题情况',
#                      operation_description="根据问卷id获取所有题目的答题情况",
#                      manual_parameters=[Parameter(name='qn_id', in_=IN_QUERY, description='问卷编号',
#                                                   type=TYPE_INTEGER, required=True)],
#                      responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
#                      )
# @api_view(['post'])
# def get_question_answer(request):
#     # 检查登录情况
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 401})
#
#     collect_form = CollectForm(request.POST)
#     if collect_form.is_valid():
#         qn_id = collect_form.cleaned_data.get('qn_id')
#
#         # 用户名是否匹配
#         try:
#             survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
#             if request.session.get('username') != survey.username:
#                 return JsonResponse({'status_code': 403})
#         except:
#             return JsonResponse({'status_code': 402})
#
#         # 所有题目的答题情况
#         questions = Question.objects.filter(survey_id=survey)
#         question_list = []
#         for question in questions:
#             answers = Answer.objects.filter(question_id=question)
#             temp = {'question_id': question.question_id, 'title': question.title, 'direction': question.direction,
#                     'must': question.is_must_answer, 'type': question.type, 'sequence': question.sequence,
#                     'right_answer': question.right_answer, 'score': question.score,
#                     'num_all': len(answers), 'options': [], 'fill_blank': [], 'scores': []}
#
#             if temp['type'] in ['radio', 'checkbox']:  # 单选，多选
#                 options = Option.objects.filter(question_id=question)
#                 for option in options:
#                     answer_option = Answer.objects.filter(question_id=question, answer__contains=option.content)
#                     answer = {'content': option.content, 'num': len(answer_option)}
#                     temp['options'].append(answer)
#
#             # elif temp['type'] == 'mark':  # 评分
#             #     max_score = question.score
#             #     for i in range(1, max_score+1):
#             #         answer_blank = answers.filter(answer=str(i))
#             #         answer = {'score': i, 'num': len(answer_blank)}
#             #         temp['scores'].append(answer)
#             else:  # 填空
#                 for item in answers:
#                     answer = {'answer_id': item.answer_id, 'content': item.answer}
#                     temp['fill_blank'].append(answer)
#             question_list.append(temp)
#         data = {'qn_id': qn_id, 'title': survey.title, 'questions': question_list}
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'status_code': 404})




@csrf_exempt
def set_finish(request):
    response = {'status_code': 1, 'message': 'success'}
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 2, 'message': '未登录'})

    if request.method == 'POST':
        finish_form = FinishForm(request.POST)
        if finish_form.is_valid():
            qn_id = finish_form.cleaned_data.get('qn_id')
            finish_time = finish_form.cleaned_data.get('finish_time')

            survey = Survey.objects.get(survey_id=qn_id)
            if not survey.is_released:
                return JsonResponse({'status_code': 3, 'message': '问卷未发布'})

            survey.finished_time = finish_time
            survey.save()
            return JsonResponse(response)

        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)

from Submit.views import get_qn_data
@csrf_exempt
def save_exam_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        qn_id = req['qn_id']# 获取问卷信息
        answer_list = req['answers']
        username = request.session.get('username')
        if username is None or username == '':
            # username = ''
            response = {'status_code': 4, 'message': '您尚未登陆'}
            return JsonResponse(response)

        survey = Survey.objects.get(survey_id=qn_id)

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

        response['questions'] = get_qn_data(qn_id)['questions']
        response['answers'] = req['answers']
        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


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
