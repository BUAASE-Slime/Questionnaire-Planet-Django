import json

import pytz
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi
import datetime

# Create your views here.
from utils.toHash import hash_code
from .form import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CollectForm
from Qn.models import *

utc = pytz.UTC

polygon_view_get_desc = '根据所选参数,获取问卷列表,默认按创建时间倒序'
polygon_view_get_parm = [
    Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号', type=TYPE_INTEGER, required=False),
    Parameter(name='is_deleted', in_=IN_QUERY, description='是否删除', type=TYPE_BOOLEAN, required=False),
    Parameter(name='title_key', in_=IN_QUERY, description='标题关键词', type=TYPE_STRING, required=False),
    Parameter(name='username', in_=IN_QUERY, description='发起人用户名', type=TYPE_STRING, required=True),
    Parameter(name='is_released', in_=IN_QUERY, description='是否发布', type=TYPE_BOOLEAN, required=False),
    Parameter(name='is_collected', in_=IN_QUERY, description='是否收藏,', type=TYPE_BOOLEAN, required=False),
    Parameter(name='order_item', in_=IN_QUERY, description='排序项,created_time-创建时间,release_time-发布时间,recycling_num-回收量',
              type=TYPE_STRING, required=False),
    Parameter(name='order_type', in_=IN_QUERY, description='排序类型,desc-倒序,asc-正序', type=TYPE_STRING, required=False),
]
polygon_view_get_resp = {200: '查询成功', 401: '未登录', 402: '查询失败', 403: '用户名不匹配,没有查询权限', 404: '表单不匹配'}


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='查询问卷列表',
                     operation_description=polygon_view_get_desc,
                     manual_parameters=polygon_view_get_parm,
                     responses=polygon_view_get_resp
                     )
@api_view(['POST'])
def get_list(request):
    # 检验是否登录
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        survey_id = request.POST.get('survey_id')
        is_deleted = bool(request.POST.get('is_deleted'))
        title_key = request.POST.get('title_key')
        username = request.POST.get('username')
        is_released = request.POST.get('is_released')
        is_collected = bool(request.POST.get('is_collected'))
        order_item = request.POST.get('order_item')
        order_type = request.POST.get('order_type')
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
                json_item = {"survey_id": survey.survey_id, "title": survey.title,
                             "description": survey.description, "is_released": survey.is_released,
                             "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                             "recycling_num": survey.recycling_num, "username": survey.username,
                             "create_time": survey.created_time.strftime("%Y/%m/%d %H:%M")}

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
        if is_released == 1:
            survey_list = survey_list.filter(is_released=is_released)
        if is_released == 0:
            print(1)
            survey_list = survey_list.filter(is_released != is_released)
        if is_collected:
            survey_list = survey_list.filter(is_collected=is_collected)
        if order_type == 'desc':
            survey_list = survey_list.order_by('-' + order_item)
        else:
            survey_list = survey_list.order_by(order_item)

        json_list = []
        for survey in survey_list:
            json_item = {"survey_id": survey.survey_id, "title": survey.title,
                         "description": survey.description, "is_released": survey.is_released,
                         "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                         "recycling_num": survey.recycling_num, "username": survey.username,
                         "create_time": survey.created_time.strftime("%Y/%m/%d %H:%M")}
            json_list.append(json_item)

        if json_list:
            return JsonResponse({'data': json.dumps(json_list, ensure_ascii=False)})
            # return JsonResponse(list(json_list), safe=False, json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'status_code': 404})


class _Params:
    USERNAME = openapi.Parameter('username', openapi.TYPE_STRING, description='用户名', type=openapi.TYPE_STRING)
    QN_ID = openapi.Parameter('qn_id', openapi.TYPE_NUMBER, description="问卷id", type=openapi.TYPE_NUMBER)


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
def create_option(question, content):
    option = Option()
    option.content = content
    question.option_num += 1
    option.question_id = question
    question.save()
    option.order = question.option_num
    option.save()


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='统计问卷回收量',
                     operation_description="返回近五日每天的回收量,周回收量和总回收量",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True), ],
                     responses=polygon_view_get_resp
                     )
@api_view(['POST'])
def get_recycling_num(request):
    # 检验是否登录
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

        submit_list = Submit.objects.filter(survey_id=survey)
        submit_list = submit_list.order_by("-submit_time")
        result = {"num_all": len(submit_list)}
        num_week = 0

        json_list = []
        dea_date = (submit_list[0].submit_time + datetime.timedelta(days=-7)).strftime("%m.%d")
        for submit in submit_list:
            submit.submit_time = submit.submit_time.strftime("%m.%d")
        date = submit_list[0].submit_time
        num = 0  # 记录每天的回收量

        for submit in submit_list:
            if submit.submit_time > dea_date:
                num_week = num_week + 1
            if submit.submit_time == date:
                num = num + 1
            else:
                json_item = {"date": date, "number": num}
                json_list.append(json_item)
                date = submit.submit_time
                num = 1

        json_item = {"date": date, "number": num}
        json_list.append(json_item)

        result['num_week'] = num_week
        result['num_day'] = json_list[:5]
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='查询全部答卷',
                     operation_description="返回用户的所有答案",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True),
                                        Parameter(name='username', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_STRING, required=True)],
                     responses=polygon_view_get_resp
                     )
@api_view(['POST'])
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
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='问卷收藏',
                     operation_description="收藏问卷",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '收藏成功', 401: '未登录', 402: '收藏失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
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
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='取消收藏',
                     operation_description="取消收藏",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
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
@swagger_auto_schema(method='post',
                     tags=['问卷相关'],
                     operation_summary='获取问卷码',
                     operation_description="根据用户的username以及问卷id得到问卷码",
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
                                                  type=TYPE_INTEGER, required=True)],
                     responses={200: '操作成功', 401: '未登录', 402: '操作失败', 403: '用户名不匹配,没有查询权限', 404: '表单格式不正确'}
                     )
@api_view(['post'])
def get_code(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    collect_form = CollectForm(request.POST)
    if collect_form.is_valid():
        survey_id = collect_form.cleaned_data.get('survey_id')

        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
            if survey.question_num == 0:
                return JsonResponse({'status_code': 402, 'msg': "no_questions"})
            if request.session.get('username') != survey.username:
                return JsonResponse({'status_code': 403})
        except:
            return JsonResponse({'status_code': 402})

        # 生成问卷码
        code = hash_code(survey.username, str(survey_id))
        # code = hash_code(code, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        end_info = code[:20].upper()
        while Survey.objects.filter(share_url=end_info):
            code = hash_code(code, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            end_info = code[:20].upper()

        survey.share_url = end_info
        try:
            survey.save()
            data = {'code': end_info}
            return JsonResponse(data)
        except:
            return JsonResponse({'status_code': 402})

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
def get_survey_from_url(request):
    # 检查登录情况
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 401})

    if request.method == 'POST':
        response = {}
        url_form = URLForm(request.POST)
        if url_form.is_valid():
            url = url_form.cleaned_data.get('url')
            start = url.rindex('/')
            code = url[start + 1:]
            try:
                survey = Survey.objects.get(share_url=code)
                if request.session.get('username') != survey.username:
                    return JsonResponse({'status_code': 403})
            except:
                return JsonResponse({'status_code': 402})

            response['title'] = survey.title
            response['description'] = survey.description
            response['type'] = survey.type
            response['question_num'] = survey.question_num
            response['created_time'] = survey.created_time
            response['is_released'] = survey.is_released
            response['release_time'] = survey.release_time
            response['finished_time'] = survey.finished_time
            response['recycling_num'] = survey.recycling_num

            question_list = Question.objects.filter(survey_id=survey.survey_id)
            questions = []
            for item in question_list:
                temp = {}
                temp['question_id'] = item.question_id
                temp['title'] = item.title
                temp['direction'] = item.direction
                temp['must'] = item.is_must_answer
                temp['type'] = item.type
                temp['qn_id'] = survey.survey_id
                temp['sequence'] = item.sequence
                temp['id'] = item.sequence  # 按照前端的题目顺序
                temp['option'] = []
                temp['answer'] = ''
                if temp['type'] in ['radio', 'checkbox']:
                    # 单选题或者多选题有选项
                    option_list = Option.objects.filter(question_id=item.question_id)
                    for option_item in option_list:
                        option_dict = {}
                        option_dict['option_id'] = option_item.option_id
                        option_dict['title'] = option_item.content
                        temp['option'].append(option_dict)

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
                     manual_parameters=[Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号',
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
        survey_id = collect_form.cleaned_data.get('survey_id')

        # 用户名是否匹配
        try:
            survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
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
                    'num_all': len(answers), 'options': [], 'fill_blank': [], 'scores': []}

            if temp['type'] in ['radio', 'checkbox']:  # 单选，多选
                options = Option.objects.filter(question_id=question)
                for option in options:
                    answer_option = Answer.objects.filter(question_id=question, answer__contains=option.content)
                    answer = {'content': option.content, 'num': len(answer_option)}
                    temp['options'].append(answer)

            elif temp['type'] == 'mark':  # 评分
                max_score = question.score
                for i in range(1, max_score+1):
                    answer_blank = answers.filter(answer=str(i))
                    answer = {'score': i, 'num': len(answer_blank)}
                    temp['scores'].append(answer)
            else:  # 填空
                for item in answers:
                    answer = {'answer_id': item.answer_id, 'content': item.answer}
                    temp['fill_blank'].append(answer)
            question_list.append(temp)
        data = {'qn_id': survey_id, 'title': survey.title, 'questions': question_list}
        return JsonResponse(data)
    else:
        return JsonResponse({'status_code': 404})


@csrf_exempt
def save_qn_answer(request):
    response = {'status_code': 1, 'message': 'success'}
    username = request.session.get('username')
    if request.method == 'POST':
        req = json.loads(request.body)
        # print(req)
        qn_id = req['qn_id']

        survey = Survey.objects.get(survey_id=qn_id, is_deleted=False)
        survey.recycling_num = survey.recycling_num + 1
        survey.save()

        submit = Submit(survey_id=survey)
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
