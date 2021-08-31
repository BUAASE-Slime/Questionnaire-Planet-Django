import datetime
import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CreateNewQnForm
from Qn.models import Survey, Submit, Question, Answer, Option
from djangoProject.settings import WEB_ROOT
from epidemic.form import *
# from signup.views import question_dict_to_question, create_question_in_save, OptionRecyleNumError
from userinfo.models import User





@csrf_exempt
def save_epidemic_answer_by_code(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        req = json.loads(request.body)
        code = req['code']  # 获取问卷信息
        answer_list = req['answers']
        username = request.session.get('username')
        if username is None:
            username = ''
        print("username" + username)
        survey = Survey.objects.get(share_url=code)
        if survey.is_deleted:
            response = {'status_code': 2, 'message': '问卷已删除'}
            return JsonResponse(response)

            # if time.mktime(survey.finished_time.timetuple()) < time.time():
            #     return JsonResponse({'status_code': -1, 'message': '超过截止时间'})

        # if Submit.objects.filter(survey_id=survey, username=username) and username != '':  # TODO delete
        #     return JsonResponse({'status_code': 3, 'message': '已提交过问卷'})
        if Submit.objects.filter(survey_id=survey, username=username,
                                 submit_time__gte=datetime.datetime.today().date()):
            response = {'status_code': 999, 'message': '当天已填写'}
            return JsonResponse(response)

        if not survey.is_released:
            return JsonResponse({'status_code': 4, 'message': '问卷未发布'})

        survey.recycling_num = survey.recycling_num + 1
        survey.save()

        submit = Submit(username=username, survey_id=survey, score=0)
        submit.save()
        for answer_dict in answer_list:
            question = Question.objects.get(question_id=answer_dict['question_id'])
            answer = Answer(answer=answer_dict['answer'], username=username,
                            type=answer_dict['type'], question_id=question, submit_id=submit)
            answer.save()

        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)





def compare_location(id):
    submit = Submit.objects.get(submit_id=id)
    submit_list = Submit.objects.filter(username=submit.username, survey_id=submit.survey_id,
                                        submit_time__lte=submit.submit_time)
    submit_list = submit_list.order_by('-submit_time')
    if submit_list.count() == 1:
        return JsonResponse({'status_code': -1, 'message': '第一次提交'})
    last_submit = submit_list[1]
    answer = Answer.objects.get(submit_id=submit, type='location')
    last_answer = Answer.objects.get(submit_id=last_submit, type='location')
    print("location:" + answer.answer + "/ last_location:" + last_answer.answer)
    if answer.answer == last_answer.answer:
        return JsonResponse({'status_code': 1, 'message': '位置相同'})
    else:
        return JsonResponse({'status_code': 2, 'message': '位置不同'})


high_risk = ["河南省 商丘市 虞城县", "云南省 德宏傣族景颇族自治州 瑞丽市"]
middle_risk = ["上海市 松江区", "上海市 浦东新区", "云南省 瑞丽市", "湖北省 荆门市 掇刀区", "河南省 郑州市 二七区",
               "河南省 商丘市", "河南省 开封市 尉氏县", "江苏省 扬州市 蜀区-瘦西湖风景名胜区", "江苏省 扬州市 广陵区",
               "江苏省 扬州市 邗江区", "江苏省 扬州市 经济技术开发区"]


def judge_location(id):
    submit = Submit.objects.get(submit_id=id)
    answer = Answer.objects.get(submit_id=submit, type='location')
    location = answer.answer
    high_data = [x for i, x in enumerate(high_risk) if x.find(location) != -1]
    middle_data = [x for i, x in enumerate(middle_risk) if x.find(location) != -1]
    print('high_data:'+"/".join(high_data))
    print('middle_data:'+"/".join(middle_data))
    if len(high_data) == 0 and len(middle_data) == 0:
        return JsonResponse({'status_code': 1, 'message': '低风险地区'})
    if len(high_data) != 0:
        return JsonResponse({'status_code': 2, 'message': '高风险地区'})
    if len(middle_data) != 0:
        return JsonResponse({'status_code': 3, 'message': '中风险地区'})

def test(request):
    if request.method == 'POST':
        form = GetForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('question_id')
            return judge_location(id)
