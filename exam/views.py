# Create your views here.
import json
import time

import pytz
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
import datetime

# Create your views here.
from Submit.views import produce_time, create_option
from exam.forms import *
from utils.toHash import hash_code
# from .form import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.models import *



@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='查询全部答卷',
                     operation_description="返回用户的所有答案",
                     manual_parameters=[Parameter(name='qn_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True),
                                        Parameter(name='username', in_=IN_QUERY, description='用户名',
                                                  type=TYPE_STRING, required=True)],
                     responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['POST'])
def get_answer(request):
    # 检验是否登录
    global answer_questions
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    answer_form = AnswerForm(request.POST)
    if answer_form.is_valid():
        qn_id = answer_form.cleaned_data.get('qn_id')
        username = answer_form.cleaned_data.get('username')

        # 用户名是否匹配
        if username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        # 问卷信息
        result = {}
        try:
            survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
            if username != survey.username:
                return JsonResponse({'status_code': 403})
        except:
            return JsonResponse({'status_code': 402})
        result['qn_id'] = qn_id
        result['title'] = survey.title
        result['description'] = survey.description
        result['username'] = username

        # 回答信息
        result_answers = []
        questions = Question.objects.filter(survey_id=survey).order_by('sequence')
        submits = Submit.objects.filter(survey_id=survey)

        for submit in submits:
            answer_questions = {'sum_score': submit.score, 'question': []}
            for question in questions:
                answer_question = {"question_id": question.question_id, "sequence": question.sequence,
                                   "title": question.title, "direction": question.direction,
                                   "is_must_answer": question.is_must_answer, "type": question.type,
                                   'right_answer': question.right_answer}
                answer = Answer.objects.get(question_id=question, submit_id=submit)
                answer_question['answer'] = answer.answer
                answer_question['score'] = answer.score
                answer_questions['question'].append(answer_question)
            result_answers.append(answer_questions)

        result['answers'] = result_answers
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='根据链接获取问卷详细信息',
                     manual_parameters=[Parameter(name='url', in_=IN_QUERY, description='问卷链接',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
def get_qn_from_url(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        url_form = URLForm(request.POST)
        if url_form.is_valid():
            code = url_form.cleaned_data.get('code')
            try:
                survey = Survey.objects.get(share_url=code)
                if request.session.get('username') != survey.username:
                    return JsonResponse({'status_code': 403})
            except:
                return JsonResponse({'status_code': 402})

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
            response['recycling_num'] = survey.recycling_num

            question_list = Question.objects.filter(survey_id=survey.survey_id)
            questions = []
            for item in question_list:
                temp = {}
                temp['question_id'] = item.question_id
                temp['row'] = item.raw
                temp['score'] = item.score
                temp['title'] = item.title
                temp['direction'] = item.direction
                temp['must'] = item.is_must_answer
                temp['type'] = item.type
                temp['qn_id'] = survey.survey_id
                temp['sequence'] = item.sequence
                temp['id'] = item.sequence  # 按照前端的题目顺序
                temp['options'] = []
                temp['answer'] = item.right_answer
                if temp['type'] in ['radio', 'checkbox']:
                    # 单选题或者多选题有选项
                    option_list = Option.objects.filter(question_id=item.question_id)
                    for option_item in option_list:
                        option_dict = {}
                        option_dict['id'] = option_item.option_id
                        option_dict['title'] = option_item.content
                        temp['options'].append(option_dict)

                else:  # TODO 填空题或者其他
                    pass

                questions.append(temp)
                print(questions)
            response['questions'] = questions
            return JsonResponse(response)
        else:
            return JsonResponse({'status_code': 404})
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='获取题目答题情况',
                     operation_description="根据问卷id获取所有题目的答题情况",
                     manual_parameters=[Parameter(name='qn_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
def get_question_answer(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        qn_id = collect_form.cleaned_data.get('qn_id')

        # 用户名是否匹配
        try:
            survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
            if request.session.get('username') != survey.username:
                return JsonResponse({'status_code': 403})
        except:
            return JsonResponse({'status_code': 402})

        # 所有题目的答题情况
        questions = Question.objects.filter(survey_id=survey)
        question_list = []
        for question in questions:
            answers = Answer.objects.filter(question_id=question)
            temp = {'question_id': question.question_id, 'title': question.title, 'direction': question.direction,
                    'must': question.is_must_answer, 'type': question.type, 'sequence': question.sequence,
                    'right_answer': question.right_answer, 'score': question.score,
                    'num_all': len(answers), 'options': [], 'fill_blank': [], 'scores': []}

            if temp['type'] in ['radio', 'checkbox']:  # 单选，多选
                options = Option.objects.filter(question_id=question)
                for option in options:
                    answer_option = Answer.objects.filter(question_id=question, answer__contains=option.content)
                    answer = {'content': option.content, 'num': len(answer_option)}
                    temp['options'].append(answer)

            # elif temp['type'] == 'mark':  # 评分
            #     max_score = question.score
            #     for i in range(1, max_score+1):
            #         answer_blank = answers.filter(answer=str(i))
            #         answer = {'score': i, 'num': len(answer_blank)}
            #         temp['scores'].append(answer)
            else:  # 填空
                for item in answers:
                    answer = {'answer_id': item.answer_id, 'content': item.answer}
                    temp['fill_blank'].append(answer)
            question_list.append(temp)
        data = {'qn_id': qn_id, 'title': survey.title, 'questions': question_list}
        return JsonResponse(data)
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
def save_qn_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 2, 'message': '未登录'})
    username = request.session.get('username')
    if request.method == 'POST':
        req = json.loads(request.body)
        # print(req)
        qn_id = req['qn_id']

        survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
        if time.mktime(survey.finished_time.timetuple()) < time.time():
            return JsonResponse({'status_code': -1, 'message': '超过截止时间'})

        if Submit.objects.filter(survey_id=survey, username=username):
            return JsonResponse({'status_code': 3, 'message': '已提交过问卷'})

        if not survey.is_released:
            return JsonResponse({'status_code': 4, 'message': '问卷未发布'})

        survey.recycling_num = survey.recycling_num + 1
        survey.save()

        submit = Submit(survey_id=survey)
        submit.username = username
        submit.save()

        answer_list = req['answers']
        sum_score = 0
        question_score = []
        for item in answer_list:
            if item['answer'] is None:
                continue
            answer = Answer(question_id_id=item['question_id'], submit_id_id=submit.submit_id,
                            answer=item['answer'], type=item['type'])
            question = Question.objects.get(question_id=item['question_id'])
            score = question.score
            result = "正确"
            if question.right_answer != item['answer'] and question.right_answer != "":
                score = 0
                result = "错误"

            sum_score = sum_score + score
            answer.score = score
            answer.username = username
            answer.save()
            data = {'question_id': question.question_id, 'title': question.title,
                    'score': score, 'right_answer': question.right_answer,
                    'your_answer': item['answer'], 'result': result}
            question_score.append(data)

        submit.score = sum_score
        submit.save()

        response['sum_score'] = sum_score
        response['question_score'] = question_score

        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)


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


@csrf_exempt
def create_qn(request):
    global survey
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        new_qn_form = CreateNewQuestionForm(request.POST)
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
                question.raw = new_question_form.cleaned_data.get('row')
                question.score = new_question_form.cleaned_data.get('score')
                question.right_answer = new_question_form.cleaned_data.get('right_answer')

                option_str = new_question_form.cleaned_data.get('options')
            except:
                response = {'status_code': -3, 'message': '后端炸了'}
                return JsonResponse(response)
            KEY = "-<^-^>-"
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
        print(req['finish_time'])
        if req['finish_time'] != '' and req['finish_time'] is not None:
            survey.finished_time = req['finish_time']
        survey.save()
        question_list = req['questions']

        if request.session.get("username") != req['username']:
            request.session.flush()
            return JsonResponse({'status_code': 0})

        # TODO
        question_num = 0
        for question in question_list:
            question_num += 1
            create_question_in_save(question['title'], question['description'], question['must']
                                    , question['type'], qn_id=req['qn_id'], raw=question['row'],
                                    score=question['score'],
                                    options=question['options'],
                                    sequence=question['id'],
                                    right_answer=question['refer'],
                                    )

        survey.question_num = question_num
        survey.save()
        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}


def create_question_in_save(title, direction, must, type, qn_id, raw, score, options, sequence, right_answer):
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
        question.right_answer = right_answer
    except:
        response = {'status_code': -3, 'message': '后端炸了'}
        return JsonResponse(response)

    option_list = options
    for item in option_list:
        print(item)
        content = item['title']
        sequence = item['id']
        create_option(question, content, sequence)
    question.save()

def save_exam_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        title = req['title']
        qn_id = req['qn_id']# 获取问卷信息
        answer_list = req['answers']
        username = request.session.get('username')
        if username is None:
            username = ''

        survey = Survey.objects.get(survey_id=qn_id)
        submit = Submit(username=username, survey_id=survey,score=0)
        submit.save()
        for answer_dict in answer_list:
            question = Question.objects.get(question_id=answer_dict['question_id'])
            answer = Answer(anwer=answer_dict['ans'],username=username,
                            type = answer_dict['type'],question_id=question,submit_id=submit,
                            score=answer_dict['score']
                            )
            answer.save()

        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)
