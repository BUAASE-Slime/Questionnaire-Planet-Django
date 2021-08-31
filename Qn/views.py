import json

import pytz
import datetime
import random

# Create your views here.
from utils.toHash import hash_code
from .form import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CollectForm
from Qn.models import *

utc = pytz.UTC
KEY_STR = "-<^-^>-"

@csrf_exempt
def get_list(request):
    # 检验是否登录
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})
    print("user login")

    if request.method == 'POST':
        survey_id = request.POST.get('survey_id')
        is_deleted = bool(request.POST.get('is_deleted'))
        title_key = request.POST.get('title_key')
        username = request.POST.get('username')
        is_released = request.POST.get('is_released')
        is_collected = bool(request.POST.get('is_collected'))
        order_item = request.POST.get('order_item')
        order_type = request.POST.get('order_type')
        qn_type = request.POST.get('type')

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
                num = len(Submit.objects.filter(survey_id=survey))
                json_item = {"survey_id": survey.survey_id, "title": survey.title,
                             "description": survey.description, "is_released": survey.is_released,
                             "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                             "recycling_num": num, "username": survey.username,
                             "create_time": survey.created_time.strftime("%Y-%m-%d %H:%M"),
                             "type": survey.type}

                print(json_item)
                return JsonResponse(json_item)
            except:
                return JsonResponse({'status_code': 402})

        survey_list = Survey.objects.all()
        if is_deleted:
            survey_list = survey_list.filter(is_deleted=is_deleted)
        else:
            survey_list = survey_list.filter(is_deleted=False)
        if title_key:
            survey_list = survey_list.filter(title__contains=title_key)
        if username:
            survey_list = survey_list.filter(username=username)
        if is_released == 1 or is_released == '1':
            survey_list = survey_list.filter(is_released=True)
        if is_released == 0 or is_released == '0':

            survey_list = survey_list.filter(is_released=False)
        if is_collected:
            survey_list = survey_list.filter(is_collected=is_collected)
        if order_type == 'desc':
            survey_list = survey_list.order_by('-' + order_item)
        else:
            survey_list = survey_list.order_by(order_item)
        if qn_type:
            if qn_type != '0':
                survey_list = survey_list.filter(type=qn_type)

        json_list = []
        for survey in survey_list:
            num = len(Submit.objects.filter(survey_id=survey))
            json_item = {"survey_id": survey.survey_id, "title": survey.title,
                         "description": survey.description, "is_released": survey.is_released,
                         "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                         "recycling_num": num, "username": survey.username,
                         "create_time": survey.created_time.strftime("%Y-%m-%d %H:%M"),
                         "type": survey.type}
            json_list.append(json_item)

        if json_list:
            return JsonResponse({'data': json.dumps(json_list, ensure_ascii=False)})
            # return JsonResponse(list(json_list), safe=False, json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'status_code': 404})


@csrf_exempt
def all_submittion_count(request):
    if request.method == 'POST':
        try:
            count = int(Submit.objects.all().count())
        except:
            return JsonResponse({'status_code': -1, 'message': "后端炸了"})
        return JsonResponse({'status_code': 1, 'count': count, 'message': "success"})
    else:
        return JsonResponse({'status_code': 0, 'count': 0, 'message': "请求错误"})



@csrf_exempt
def get_answer(request):
    # 检验是否登录
    global answer_questions
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    answer_form = AnswerForm(request.POST)
    if answer_form.is_valid():
        survey_id = answer_form.cleaned_data.get('survey_id')
        username = answer_form.cleaned_data.get('username')

        # 用户名是否匹配
        if username != request.session.get('username'):
            return JsonResponse({'status_code': 403})

        # 问卷信息
        result = {}
        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
            if username != survey.username:
                return JsonResponse({'status_code': 403})
        except:
            return JsonResponse({'status_code': 402})
        result['survey_id'] = survey_id
        result['title'] = survey.title
        result['description'] = survey.description
        result['username'] = username

        # 回答信息
        result_answers = []
        questions = Question.objects.filter(survey_id=survey).order_by('sequence')
        submits = Submit.objects.filter(survey_id=survey)

        for submit in submits:
            answer_questions = []
            for question in questions:
                answer_question = {"question_id": question.question_id, "sequence": question.sequence,
                                   "title": question.title, "direction": question.direction,
                                   "is_must_answer": question.is_must_answer, "type": question.type}
                answer = Answer.objects.get(question_id=question, submit_id=submit)
                answer_question['answer'] = answer.answer
                answer_questions.append(answer_question)
            result_answers.append(answer_questions)

        result['answers'] = result_answers
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
def collect(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
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
def not_collect(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
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


@csrf_exempt
def get_code(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')

        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
            print(survey.question_num)
            if survey.question_num == 0:
                return JsonResponse({'status_code': 402, 'msg': "no_questions"})
            if request.session.get('username') != survey.username:
                return JsonResponse({'status_code': 403})
        except:
            return JsonResponse({'status_code': 402})

        if survey.is_released:
            return JsonResponse({'status_code': 406})
        if survey.share_url != '':
            data = {'code': survey.share_url, 'status_code': 200}
            return data

        # 生成问卷码
        code = hash_code(survey.username, str(survey_id))
        # code = hash_code(code, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        end_info = code[:20].upper()
        while Survey.objects.filter(share_url=end_info):
            code = hash_code(code, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            end_info = code[:20].upper()

        survey.share_url = end_info
        try:
            survey.is_released = True
            survey.save()
            data = {'code': end_info, 'status_code': 200}
            return JsonResponse(data)
        except:
            return JsonResponse({'status_code': 402})

    else:
        return JsonResponse({'status_code': 404})

@csrf_exempt
def get_code_existed(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 0})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')

        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
            if request.session.get('username') != survey.username:
                return JsonResponse({'status_code': 0})
        except:
            return JsonResponse({'status_code': 2})

        if not survey.is_released:
            return JsonResponse({'status_code': 2})
        if survey.share_url:
            return JsonResponse({'status_code': 1, 'code': survey.share_url})
        return JsonResponse({'status_code': 2})

    else:
        return JsonResponse({'status_code': 2})


@csrf_exempt
def save_qn_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    username = request.session.get('username')
    if request.method == 'POST':
        req = json.loads(request.body)
        print(req)
        code = req['code']

        try:
            survey = Survey.objects.get(share_url=code)
        except:
            return JsonResponse({'status_code': 3})
        if survey.is_deleted or not survey.is_released:
            return JsonResponse({'status_code': 2})
        survey.recycling_num = survey.recycling_num + 1
        survey.save()

        submit = Submit(survey_id=survey)
        if username:
            submit.username = username
        submit.save()

        answer_list = req['answers']
        for item in answer_list:
            if item['answer']:
                print(item['answer'])

                answer_str = str(item['answer'])

                # answer_str.replace(KEY_STR, ";")
                # the_answer = ";".join(str(i) for i in answer_str.split(KEY_STR))
                # print(the_answer)
                print(answer_str.split(KEY_STR))
                print(answer_str)
                answer = Answer(question_id_id=item['question_id'], submit_id_id=submit.submit_id,
                            answer=answer_str, type=item['type'])
                if username:
                    answer.username = username
                answer.save()
        response['submit_id'] = submit.submit_id

        return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)


@csrf_exempt
def change_code(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('qn_id')
            try:
                qn = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': 2, 'message': '问卷不存在'}
                return JsonResponse(response)
            # TODO
            # username = qn.username
            # if request.session['username'] != username:
            #     response = {'status_code': 0, 'message': '没有访问权限'}
            #     return JsonResponse(response)

            if qn.share_url == '':
                response = {'status_code': 3, 'message': '尚未存在分享链接'}
                return JsonResponse(response)
            raw_code = hash_code(qn.username, str(id))
            code = ""
            raw_code_len = len(raw_code)
            for i in range(20):
                code += raw_code[random.randint(0, raw_code_len - 1)]
            qn.share_url = code
            qn.save()

            return JsonResponse({'status_code': 1, 'code': code})

        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)
