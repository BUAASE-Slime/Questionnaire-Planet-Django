import json
import time

import pytz
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from Qn.form import CreateNewQnForm, SurveyIdForm
from Qn.models import *
# Create your views here.
from Submit.views import produce_time,finish_qn

utc = pytz.UTC
class SubmitRecyleNumError(Exception):
    def __init__(self,num):
        self.num = num

    def __str__(self):
        return "您报名的问卷回收数目为： %d, 已达到最大回收量" % self.num

class OptionRecyleNumError(BaseException):
    def __init__(self,num):
        self.num = num

    def __str__(self):
        return "您报名的选项回收数目为： %d, 已达到最大回收量" % self.num


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
def save_signup_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        qn_id = req['qn_id']  # 获取问卷信息
        answer_list = req['answers']
        username = request.session.get('username')
        if username is None:
            username = ''
        print("username"+username)
        survey = Survey.objects.get(survey_id=qn_id)
        if survey.is_deleted:
            response = {'status_code': 2, 'message': '问卷已删除'}
            return JsonResponse(response)

            # if time.mktime(survey.finished_time.timetuple()) < time.time():
            #     return JsonResponse({'status_code': -1, 'message': '超过截止时间'})

        if Submit.objects.filter(survey_id=survey, username=username) and username != '':#TODO delete
            return JsonResponse({'status_code': 3, 'message': '已提交过问卷'})

        if not survey.is_released:
            return JsonResponse({'status_code': 4, 'message': '问卷未发布'})

        if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
            finish_qn(qn_id)
            return JsonResponse({'status_code': 5, 'message': '人数已满'})
        sum_option_count = 0
        has_signup = False
        question_list = Question.objects.filter(survey_id=survey)
        for question in question_list:
            option_list = Option.objects.filter(question_id=question)
            for option in option_list:
                if option.has_num_limit:
                    sum_option_count += option.remain_num
                    has_signup = True
        if sum_option_count == 0 and has_signup:
            finish_qn(qn_id)
            return JsonResponse({'status_code': 5, 'message': '人数已满'})

        try:
            with transaction.atomic():
                if survey.recycling_num + 1 > survey.max_recycling:
                    raise SubmitRecyleNumError(survey.recycling_num)
                survey.recycling_num = survey.recycling_num + 1
                survey.save()


        except SubmitRecyleNumError as e:
            print('问卷报名已满,错误信息为',e)
            finish_qn(qn_id)
            return JsonResponse({'status_code': 11, 'message': '问卷报名已满'})

        submit = Submit(username=username, survey_id=survey, score=0)
        submit.save()
        for answer_dict in answer_list:
            question = Question.objects.get(question_id=answer_dict['question_id'])
            answer = Answer(answer=answer_dict['ans'], username=username,
                            type=answer_dict['type'], question_id=question, submit_id=submit)
            if question.type in ["radio", "checkbox"]:
                option = Option.objects.get(content=answer_dict['ans'],question_id=question)
                try:
                    with transaction.atomic():
                        if option.remain_num <=0:
                            raise OptionRecyleNumError(option.num_limit)
                    option.remain_num = option.remain_num - 1
                    option.save()
                except OptionRecyleNumError as e:
                    print('问卷存在报名项目报名已满,错误信息为', e)
                    # finish_qn(qn_id)
                    return JsonResponse({'status_code': 12, 'message': '有选项报名已满'})

            answer.save()

        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def save_signup_answer_by_code(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        code = req['code']
        answer_list = req['answers']
        username = request.session.get('username')
        if username is None:
            username = ''
        print("username"+username)
        survey = Survey.objects.get(share_url=code)
        if survey.is_deleted:
            response = {'status_code': 2, 'message': '问卷已删除'}
            return JsonResponse(response)

            # if time.mktime(survey.finished_time.timetuple()) < time.time():
            #     return JsonResponse({'status_code': -1, 'message': '超过截止时间'})

        if Submit.objects.filter(survey_id=survey, username=username) and username != '':#TODO delete
            return JsonResponse({'status_code': 3, 'message': '已提交过问卷'})

        if not survey.is_released:
            return JsonResponse({'status_code': 4, 'message': '问卷未发布'})

        if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
            finish_qn(survey.survey_id)
            return JsonResponse({'status_code': 5, 'message': '人数已满'})
        try:
            with transaction.atomic():
                if survey.recycling_num + 1 > survey.max_recycling:
                    raise SubmitRecyleNumError(survey.recycling_num)
                survey.recycling_num = survey.recycling_num + 1
                survey.save()

        except SubmitRecyleNumError as e:
            print('问卷报名已满,错误信息为',e)
            finish_qn(survey.survey_id)
            return JsonResponse({'status_code': 11, 'message': '问卷报名已满'})

        submit = Submit(username=username, survey_id=survey, score=0)
        submit.save()
        for answer_dict in answer_list:
            question = Question.objects.get(question_id=answer_dict['question_id'])
            answer = Answer(answer=answer_dict['answer'], username=username,
                            type=answer_dict['type'], question_id=question, submit_id=submit)
            if question.type in ["radio", "checkbox"]:
                options = Option.objects.filter(question_id=question)
                from Submit.views import KEY_STR
                print(answer_dict)
                option_content_list = answer_dict['answer'].split(KEY_STR)
                for option in options:
                    if option.content in option_content_list:
                        try:
                            with transaction.atomic():
                                if option.remain_num <=0:
                                    raise OptionRecyleNumError(option.num_limit)
                            option.remain_num = option.remain_num - 1
                            option.save()
                        except OptionRecyleNumError as e:
                            print('问卷存在报名项目报名已满,错误信息为', e)
                            finish_qn(survey.survey_id)
                            return JsonResponse({'status_code': 12, 'message': '有选项报名已满'})

            answer.save()

        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
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
                              "must": True, "description": '', "row": 1, "score": 0,
                              "options": [{'id': 1, 'title': ""}]},
                             {"id": 2, "type": "text", "title": "你的手机号是：",
                              "must": True, "description": '', "row": 1, "score": 0,
                              "options": [{'id': 1, 'title': ""}]}]

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
            try:
                survey.max_recycling = req['max_recycling']
            except:
                pass
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
        return JsonResponse(response)


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
            remain_num = item['supply'] - item['consume']
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
            try:
                has_num_limit = item['hasNumLimit']
                num_limit = item['supply']
                remain_num = item['supply'] - item['consume']
            except:
                has_num_limit = False
                num_limit = 10000
                remain_num = 10000
        create_option(question, content, sequence, has_num_limit, num_limit, remain_num)
    question.save()


