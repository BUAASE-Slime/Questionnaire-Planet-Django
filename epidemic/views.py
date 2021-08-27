import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Qn.form import CreateNewQnForm
from Qn.models import Survey, Submit, Question
from signup.views import question_dict_to_question, create_question_in_save
from userinfo.models import User


@csrf_exempt
def create_qn_epidemic(request):
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
            if type == '5':
                description = "这里是疫情打卡问卷说明信息，您可以在此处编写关于本考试问卷的简介，帮助填写者了解这份问卷。"
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

            # 疫情打卡问卷问题模板
            if type == '5':
                questions = []
                questions.append({"id": 1, "type": "text", "title": "你的学号是：",
                                  "must": True, "description": '', "row": 1, "score": 0,
                                  "options": [{'id': 1, 'title': ""}]}),
                questions.append({"id": 2, "type": "text", "title": "你的姓名是：",
                                  "must": True, "description": '', "row": 1, "score": 0,
                                  "options": [{'id': 1, 'title': ""}]})
                questions.append({"id": 3, "type": "radio", "title": "你的体温是：",
                                  "must": True, "description": '', "row": 1, "score": 0,
                                  "options": [{"title": "36℃以下", "id": 1},
                                              {"title": "36.0℃~37.0℃", "id": 2},
                                              {"title": "37.1℃~38.0℃", "id": 3},
                                              {"title": "38.1℃~39.0℃", "id": 4},
                                              {"title": "39℃以上", "id": 5}]})
                questions.append({"id": 4, "type": "radio", "title": "近14日内，所接触环境和人员是否一切正常？",
                                  "must": True, "description": '', "row": 1, "score": 0,
                                  "options": [{"title": "是（未接触风险地区和人员，无入境共居成员，社区无确诊）", "id": 1},
                                              {"title": "否", "id": 2}]})
                questions.append({"id": 5, "type": "radio", "title": "今日本人情况是否正常？",
                                  "must": True, "description": '', "row": 1, "score": 0,
                                  "options": [{"title": "是（本人健康且未处于隔离期）", "id": 1},
                                              {"title": "否", "id": 2}]})
                questions.append({"id": 6, "type": "location", "title": "所在地点",
                                  "must": True, "description": '', "row": 1, "score": 0,
                                  "options": [{'id': 1, 'title': ""}]})

                response['questions'] = questions

            response['qn_id'] = survey.survey_id
            return JsonResponse(response)
        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': 'invalid http method'}
        return JsonResponse(response)

