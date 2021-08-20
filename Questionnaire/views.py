from django.shortcuts import render

# Create your views here.
from .form import *
from .models import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def all_submittion_count(request):
    if request.method == 'POST':
        try:
            count = int(Submit.objects.all().count())
        except :
            return JsonResponse({'status_code': 1,})
        return JsonResponse({'status_code': 1, 'count': count})
    else:
        return JsonResponse({'status_code': 0, 'count': 0,})

@csrf_exempt
def delete_survey(request):
    response = {'status_code': 1, 'msg': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': -1, 'msg': '问卷不存在'}
                return JsonResponse(response)
            survey.is_deleted = True
            # 是否真的删掉呢
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'msg': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def get_survey_details(request):
    response = {'status_code': 1, 'msg': 'success'}
    if request.method == 'POST':
        survey_form = SurveyIdForm(request.POST)
        if survey_form.is_valid():
            id = survey_form.cleaned_data.get('survey_id')
            try:
                survey = Survey.objects.get(survey_id=id)
            except:
                response = {'status_code': -2, 'msg': '问卷不存在'}
                return JsonResponse(response)

            response['title'] = survey.title
            response['subtitle'] = survey.subtitle
            response['type'] = survey.type
            response['question_num'] = survey.question_num
            response['created_time'] = survey.created_time
            response['is_released'] = survey.is_released
            response['release_time'] = survey.release_time
            response['finished_time'] = survey.finished_time
            response['recycling_num'] = survey.recycling_num

            question_list = Question.objects.filter(survey_id=id)
            questions = []
            for item in question_list:
                temp = {}
                temp['question_id'] = item.question_id
                temp['title'] = item.title
                temp['direction'] = item.direction
                temp['is_must_answer'] = item.is_must_answer
                temp['type'] = item.type
                temp['survey_id'] = item.survey_id
                temp['sequence'] = item.sequence
                temp['option'] = []
                if temp['type'] < 2:
                # 单选题或者多选题有选项
                    option_list = Option.objects.filter(question_id=item.question_id)
                    for option_item in option_list:
                        option_dict = {}
                        option_dict['option_id'] = option_item.option_id
                        option_dict['content'] = option_item.content
                        temp['option'].append(option_dict)
                    temp['answer']  = ''
                questions.append(temp)
            response['questions'] = questions

            return JsonResponse(response)


        else:
            response = {'status_code': -1, 'msg': '问卷id不为整数'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'msg': '请求错误'}
        return JsonResponse(response)

@csrf_exempt
def delete_question(request):
    response = {'status_code': 1, 'msg': 'success'}
    if request.method == 'POST':
        question_form = QuestionIdForm(request.POST)
        if question_form.is_valid():
            id = question_form.cleaned_data.get('question_id')
            try:
                question = Question.objects.get(question_id=id)
            except:
                response = {'status_code': -1, 'msg': '题目不存在'}
                return JsonResponse(response)
            question.delete()
            # 是否真的删掉呢
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'msg': '请求错误'}
        return JsonResponse(response)
