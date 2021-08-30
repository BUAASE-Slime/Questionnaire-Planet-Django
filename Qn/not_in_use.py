
from django.utils import timezone


# @csrf_exempt
# def get_recycling_num(request):
#     # 检验是否登录
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 401})
#
#     collect_form = CollectForm(request.POST)
#     if collect_form.is_valid():
#         survey_id = collect_form.cleaned_data.get('survey_id')
#         try:
#             survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
#         except:
#             return JsonResponse({'status_code': 402})
#
#         print(survey_id)
#
#         # 检查用户名是否匹配
#         if survey.username != request.session.get('username'):
#             return JsonResponse({'status_code': 403})
#
#         submit_list = Submit.objects.filter(survey_id=survey)
#         submit_list = submit_list.order_by("-submit_time")
#         result = {"num_all": len(submit_list)}
#         num_week = 0
#
#         if len(submit_list) == 0:
#             return JsonResponse({'num_all': 0, 'num_week': 0, 'num_day': 0, 'status_code': 200})
#
#         json_list = []
#         dea_date = (timezone.now() + datetime.timedelta(days=-7)).strftime("%m.%d")
#         for submit in submit_list:
#             submit.submit_time = submit.submit_time.strftime("%m.%d")
#         date = submit_list[0].submit_time
#         num = 0  # 记录每天的回收量
#
#         datelist = []
#         numlist = []
#
#         for submit in submit_list:
#             if submit.submit_time > dea_date:
#                 num_week = num_week + 1
#             if submit.submit_time == date:
#                 num = num + 1
#             else:
#                 json_item = {"date": date, "number": num}
#                 datelist.append(date)
#                 numlist.append(num)
#                 json_list.append(json_item)
#                 date = submit.submit_time
#                 num = 1
#
#         json_item = {"date": date, "number": num}
#         json_list.append(json_item)
#
#         result['num_week'] = num_week
#         result['num_day'] = json_list[:5]
#         result['status_code'] = 200
#         return JsonResponse(result, safe=False)
#     else:
#         return JsonResponse({'status_code': 404})

#
# @csrf_exempt
# def get_recycling_num_total(request):
#     # 检验是否登录
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 401})
#
#     collect_form = CollectForm(request.POST)
#     if collect_form.is_valid():
#         survey_id = collect_form.cleaned_data.get('survey_id')
#         try:
#             survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
#         except:
#             return JsonResponse({'status_code': 402})
#
#         # 检查用户名是否匹配
#         if survey.username != request.session.get('username'):
#             return JsonResponse({'status_code': 403})
#
#         submit_list = Submit.objects.filter(survey_id=survey)
#
#         if len(submit_list) == 0:
#             return JsonResponse({'status_code': 2})
#
#         submit_list = submit_list.order_by("-submit_time")
#         result = {"num_all": len(submit_list)}
#         num_week = 0
#
#         json_list = []
#         dea_date = submit_list[0].submit_time + datetime.timedelta(days=-7)
#         date = submit_list[0].submit_time
#
#         for submit in submit_list:
#             if submit.submit_time > dea_date:
#                 num_week = num_week + 1
#
#         result['num_week'] = num_week
#         result['num_day'] = json_list[:5]
#         result['status_code'] = 200
#         return JsonResponse(result, safe=False)
#     else:
#         return JsonResponse({'status_code': 404})



# @csrf_exempt
# def get_survey_from_url(request):
#     # 检查登录情况
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 401})
#
#     if request.method == 'POST':
#         response = {}
#         url_form = URLForm(request.POST)
#         if url_form.is_valid():
#             code = url_form.cleaned_data.get('code')
#             try:
#                 survey = Survey.objects.get(share_url=code)
#                 if request.session.get('username') != survey.username:
#                     return JsonResponse({'status_code': 403})
#             except:
#                 return JsonResponse({'status_code': 402})
#
#             response['title'] = survey.title
#             response['description'] = survey.description
#             response['type'] = survey.type
#             response['question_num'] = survey.question_num
#             response['created_time'] = survey.created_time
#             response['is_released'] = survey.is_released
#             response['release_time'] = survey.release_time
#             response['finished_time'] = survey.finished_time
#             response['recycling_num'] = survey.recycling_num
#
#             question_list = Question.objects.filter(survey_id=survey.survey_id)
#             questions = []
#             for item in question_list:
#                 temp = {}
#                 temp['question_id'] = item.question_id
#                 temp['title'] = item.title
#                 temp['description'] = item.direction
#                 temp['must'] = item.is_must_answer
#                 temp['type'] = item.type
#                 temp['qn_id'] = survey.survey_id
#                 temp['sequence'] = item.sequence
#                 temp['id'] = item.sequence  # 按照前端的题目顺序
#                 temp['option'] = []
#                 temp['answer'] = ''
#                 if temp['type'] in ['radio', 'checkbox','judge']:
#                     # 单选题或者多选题有选项
#                     option_list = Option.objects.filter(question_id=item.question_id)
#                     for option_item in option_list:
#                         option_dict = {}
#                         option_dict['option_id'] = option_item.option_id
#                         option_dict['title'] = option_item.content
#                         temp['option'].append(option_dict)
#
#                 else:  # TODO 填空题或者其他
#                     pass
#
#                 questions.append(temp)
#                 print(questions)
#             response['questions'] = questions
#
#             return JsonResponse(response)
#         else:
#             return JsonResponse({'status_code': 404})
#     else:
#         return JsonResponse({'status_code': 404})


# @csrf_exempt
# def get_question_answer(request):
#     # 检查登录情况
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 401})
#
#     collect_form = CollectForm(request.POST)
#     if collect_form.is_valid():
#         survey_id = collect_form.cleaned_data.get('survey_id')
#
#         # 用户名是否匹配
#         try:
#             survey = Survey.objects.get(survey_id=survey_id, is_deleted=False)
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
#             temp = {'question_id': question.question_id, 'title': question.title, 'description': question.direction,
#                     'must': question.is_must_answer, 'type': question.type, 'sequence': question.sequence,
#                     'num_all': len(answers), 'options': [], 'fill_blank': [], 'scores': []}
#
#             if temp['type'] in ['radio', 'checkbox','judge']:  # 单选，多选
#                 options = Option.objects.filter(question_id=question)
#                 for option in options:
#                     answer_option = Answer.objects.filter(question_id=question, answer__contains=option.content)
#                     answer = {'content': option.content, 'num': len(answer_option)}
#                     temp['options'].append(answer)
#
#             elif temp['type'] == 'mark':  # 评分
#                 max_score = question.score
#                 for i in range(1, max_score + 1):
#                     answer_blank = answers.filter(answer=str(i))
#                     answer = {'score': i, 'num': len(answer_blank)}
#                     temp['scores'].append(answer)
#             else:  # 填空
#                 for item in answers:
#                     answer = {'answer_id': item.answer_id, 'content': item.answer}
#                     temp['fill_blank'].append(answer)
#             question_list.append(temp)
#         data = {'qn_id': survey_id, 'title': survey.title, 'questions': question_list}
#         return JsonResponse(data)
#     else:
#         return JsonResponse({'status_code': 404})
