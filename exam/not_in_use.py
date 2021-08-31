
# @csrf_exempt
# def set_finish(request):
#     response = {'status_code': 1, 'message': 'success'}
#     if not request.session.get('is_login'):
#         return JsonResponse({'status_code': 2, 'message': '未登录'})
#
#     if request.method == 'POST':
#         finish_form = FinishForm(request.POST)
#         if finish_form.is_valid():
#             qn_id = finish_form.cleaned_data.get('qn_id')
#             finish_time = finish_form.cleaned_data.get('finish_time')
#
#             survey = Survey.objects.get(survey_id=qn_id)
#             if not survey.is_released:
#                 return JsonResponse({'status_code': 3, 'message': '问卷未发布'})
#
#             survey.finished_time = finish_time
#             survey.save()
#             return JsonResponse(response)
#
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': 'invalid http method'}
#         return JsonResponse(response)


# @csrf_exempt
# def save_exam_answer(request):
#     response = {'status_code': 1, 'message': 'success'}
#     if request.method == 'POST':
#         req = json.loads(request.body)
#         qn_id = req['qn_id']# 获取问卷信息
#         answer_list = req['answers']
#         username = request.session.get('username')
#         if username is None or username == '':
#             # username = ''
#             response = {'status_code': 4, 'message': '您尚未登陆'}
#             return JsonResponse(response)
#
#         survey = Survey.objects.get(survey_id=qn_id)
#
#         if survey.finished_time is not None and datetime.datetime.now() > survey.finished_time:
#             response = {'status_code': 5, 'message': '考试已结束，不允许提交'}
#             return JsonResponse(response)
#
#         survey.recycling_num += 1
#         survey.save()
#         submit = Submit(username=username, survey_id=survey,score=0)
#         submit.save()
#         all_score = 0
#         for answer_dict in answer_list:
#             question = Question.objects.get(question_id=answer_dict['question_id'])
#             answer = Answer(answer=answer_dict['answer'],username=username,
#                             type = answer_dict['type'],question_id=question,submit_id=submit,
#                             )
#             answer.save()
#             if answer_dict['answer'] == question.right_answer:
#                 answer.score = question.point
#             else:
#                 answer.score = 0
#             answer.save()
#
#             all_score += answer.score
#         submit.score = all_score
#         submit.save()
#
#         response['questions'] = get_qn_data(qn_id)['questions']
#         response['answers'] = req['answers']
#         return JsonResponse(response)
#
#     else:
#         response = {'status_code': -2, 'message': '请求错误'}
#         return JsonResponse(response)
#