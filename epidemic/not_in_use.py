
# @csrf_exempt
# def save_signup_answer(request):
#     response = {'status_code': 1, 'message': 'success'}
#     if request.method == 'POST':
#         req = json.loads(request.body)
#         qn_id = req['qn_id']  # 获取问卷信息
#         answer_list = req['answers']
#         username = request.session.get('username')
#         if username is None:
#             username = ''
#         print("username"+username)
#         survey = Survey.objects.get(survey_id=qn_id)
#         if survey.is_deleted:
#             response = {'status_code': 2, 'message': '问卷已删除'}
#             return JsonResponse(response)
#
#             # if time.mktime(survey.finished_time.timetuple()) < time.time():
#             #     return JsonResponse({'status_code': -1, 'message': '超过截止时间'})
#
#         if Submit.objects.filter(survey_id=survey, username=username) and username != '':#TODO delete
#             return JsonResponse({'status_code': 3, 'message': '已提交过问卷'})
#
#         if not survey.is_released:
#             return JsonResponse({'status_code': 4, 'message': '问卷未发布'})
#
#         if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
#             finish_qn(qn_id)
#             return JsonResponse({'status_code': 5, 'message': '人数已满'})
#         sum_option_count = 0
#         has_signup = False
#         question_list = Question.objects.filter(survey_id=survey)
#         for question in question_list:
#             option_list = Option.objects.filter(question_id=question)
#             for option in option_list:
#                 if option.has_num_limit:
#                     sum_option_count += option.remain_num
#                     has_signup = True
#         if sum_option_count == 0 and has_signup:
#             finish_qn(qn_id)
#             return JsonResponse({'status_code': 5, 'message': '人数已满'})
#
#         try:
#             with transaction.atomic():
#                 if survey.recycling_num + 1 > survey.max_recycling:
#                     raise SubmitRecyleNumError(survey.recycling_num)
#                 survey.recycling_num = survey.recycling_num + 1
#                 survey.save()
#
#
#         except SubmitRecyleNumError as e:
#             print('问卷报名已满,错误信息为',e)
#             finish_qn(qn_id)
#             return JsonResponse({'status_code': 11, 'message': '问卷报名已满'})
#
#         submit = Submit(username=username, survey_id=survey, score=0)
#         submit.save()
#         for answer_dict in answer_list:
#             question = Question.objects.get(question_id=answer_dict['question_id'])
#             answer = Answer(answer=answer_dict['ans'], username=username,
#                             type=answer_dict['type'], question_id=question, submit_id=submit)
#             if question.type in ["radio", "checkbox"]:
#                 option = Option.objects.get(content=answer_dict['ans'],question_id=question)
#                 try:
#                     with transaction.atomic():
#                         if option.remain_num <=0:
#                             raise OptionRecyleNumError(option.num_limit)
#                     option.remain_num = option.remain_num - 1
#                     option.save()
#                 except OptionRecyleNumError as e:
#                     print('问卷存在报名项目报名已满,错误信息为', e)
#                     # finish_qn(qn_id)
#                     return JsonResponse({'status_code': 12, 'message': '有选项报名已满'})
#
#             answer.save()
#
#         return JsonResponse(response)
#
#     else:
#         response = {'status_code': -2, 'message': '请求错误'}
#         return JsonResponse(response)


# @csrf_exempt
# def create_qn_epidemic(request):
#     global survey
#     response = {'status_code': 1, 'message': 'success'}
#     if request.method == 'POST':
#         new_qn_form = CreateNewQnForm(request.POST)
#         if new_qn_form.is_valid():
#             username = new_qn_form.cleaned_data.get('username')
#             title = new_qn_form.cleaned_data.get('title')
#             description = new_qn_form.cleaned_data.get('description')
#             type = new_qn_form.cleaned_data.get('type')
#
#             description = "这里是问卷说明信息，您可以在此处编写关于本问卷的简介，帮助填写者了解这份问卷。"
#             if type == '2':
#                 description = "这里是考试问卷说明信息，您可以在此处编写关于本考试问卷的简介，帮助填写者了解这份问卷。"
#             if type == '4':
#                 description = "这里是报名问卷说明信息，您可以在此处编写关于本考试问卷的简介，帮助填写者了解这份问卷。"
#             if type == '5':
#                 description = "这里是疫情打卡问卷说明信息，您可以在此处编写关于本考试问卷的简介，帮助填写者了解这份问卷。"
#             try:
#                 user = User.objects.get(username=username)
#
#             except:
#                 response = {'status_code': 2, 'message': '用户不存在'}
#                 return JsonResponse(response)
#
#             if request.session.get('username') != username:
#                 return JsonResponse({'status_code': 2})
#
#             if title == '':
#                 title = "默认标题"
#                 if type == '2':
#                     title = "默认标题"
#
#             try:
#                 survey = Survey(username=username, title=title, type=type, description=description, question_num=0,
#                                 recycling_num=0)
#                 survey.save()
#             except:
#                 response = {'status_code': -3, 'message': '后端炸了'}
#                 return JsonResponse(response)
#
#             # 疫情打卡问卷问题模板
#             if type == '5':
#                 questions = []
#                 questions.append({"id": 1, "type": "text", "title": "你的学号是：",
#                                   "must": True, "description": '', "row": 1, "score": 0,
#                                   "options": [{'id': 1, 'title': ""}]}),
#                 questions.append({"id": 2, "type": "text", "title": "你的姓名是：",
#                                   "must": True, "description": '', "row": 1, "score": 0,
#                                   "options": [{'id': 1, 'title': ""}]})
#                 questions.append({"id": 3, "type": "radio", "title": "你的体温是：",
#                                   "must": True, "description": '', "row": 1, "score": 0,
#                                   "options": [{"title": "36℃以下", "id": 1},
#                                               {"title": "36.0℃~37.0℃", "id": 2},
#                                               {"title": "37.1℃~38.0℃", "id": 3},
#                                               {"title": "38.1℃~39.0℃", "id": 4},
#                                               {"title": "39℃以上", "id": 5}]})
#                 questions.append({"id": 4, "type": "radio", "title": "近14日内，所接触环境和人员是否一切正常？",
#                                   "must": True, "description": '', "row": 1, "score": 0,
#                                   "options": [{"title": "是（未接触风险地区和人员，无入境共居成员，社区无确诊）", "id": 1},
#                                               {"title": "否", "id": 2}]})
#                 questions.append({"id": 5, "type": "radio", "title": "今日本人情况是否正常？",
#                                   "must": True, "description": '', "row": 1, "score": 0,
#                                   "options": [{"title": "是（本人健康且未处于隔离期）", "id": 1},
#                                               {"title": "否", "id": 2}]})
#                 questions.append({"id": 6, "type": "location", "title": "所在地点",
#                                   "must": True, "description": '', "row": 1, "score": 0,
#                                   "options": [{'id': 1, 'title': ""}]})
#
#                 response['questions'] = questions
#
#             response['qn_id'] = survey.survey_id
#             return JsonResponse(response)
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': 'invalid http method'}
#         return JsonResponse(response)

# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         upload_form = UploadPictureForm(request.POST, request.FILES)
#         if upload_form.is_valid():
#             question = Question.objects.get(question_id=upload_form.cleaned_data.get('question_id'))
#             question.image.delete()
#             image = upload_form.cleaned_data.get('image')
#             if image.name.split('.')[-1] not in ['jpeg', 'jpg', 'png', 'bmp', 'tif', 'gif']:
#                 return JsonResponse({'status_code': 2, 'message': '图片格式有误'})
#             question.image = image
#             question.save()
#             return JsonResponse({'status_code': 1, 'message': 'success'})
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': 'invalid http method'}
#         return JsonResponse(response)
#
#
# @csrf_exempt
# def get_image_url(request):
#     if request.method == 'POST':
#         image_form = GetForm(request.POST)
#         if image_form.is_valid():
#             question_id = image_form.cleaned_data.get('question_id')
#             question = Question.objects.get(question_id=question_id)
#             if question.image:
#                 data = WEB_ROOT + question.image.url
#             else:
#                 data = None
#             return JsonResponse({'status_code': 1, 'message': 'Success', 'data': data})
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': 'invalid http method'}
#         return JsonResponse(response)
#
#
# @csrf_exempt
# def upload_video(request):
#     if request.method == 'POST':
#         upload_form = UploadVideoForm(request.POST, request.FILES)
#         if upload_form.is_valid():
#             question = Question.objects.get(question_id=upload_form.cleaned_data.get('question_id'))
#             question.video.delete()
#             video = upload_form.cleaned_data.get('video')
#             # if video.name.split('.')[-1] not in ['mp4']:
#             #     return JsonResponse({'status_code': 2, 'message': '视频格式有误'})
#             question.video = video
#             question.save()
#             return JsonResponse({'status_code': 1, 'message': 'success'})
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': 'invalid http method'}
#         return JsonResponse(response)
#
#
# @csrf_exempt
# def get_video_url(request):
#     if request.method == 'POST':
#         video_form = GetForm(request.POST)
#         if video_form.is_valid():
#             question_id = video_form.cleaned_data.get('question_id')
#             question = Question.objects.get(question_id=question_id)
#             if question.video:
#                 data = WEB_ROOT + question.video.url
#             else:
#                 data = None
#             return JsonResponse({'status_code': 1, 'message': 'Success', 'data': data})
#         else:
#             response = {'status_code': -1, 'message': 'invalid form'}
#             return JsonResponse(response)
#     else:
#         response = {'status_code': -2, 'message': 'invalid http method'}
#         return JsonResponse(response)



#
#
# @csrf_exempt
# def save_epidemic_answer(request):
#     response = {'status_code': 1, 'message': 'success'}
#     if request.method == 'POST':
#         req = json.loads(request.body)
#         qn_id = req['qn_id']  # 获取问卷信息
#         answer_list = req['answers']
#         username = request.session.get('username')
#         if username is None:
#             username = ''
#         print("username" + username)
#         survey = Survey.objects.get(survey_id=qn_id)
#         if survey.is_deleted:
#             response = {'status_code': 2, 'message': '问卷已删除'}
#             return JsonResponse(response)
#
#             # if time.mktime(survey.finished_time.timetuple()) < time.time():
#             #     return JsonResponse({'status_code': -1, 'message': '超过截止时间'})
#
#         # if Submit.objects.filter(survey_id=survey, username=username) and username != '':  # TODO delete
#         #     return JsonResponse({'status_code': 3, 'message': '已提交过问卷'})
#         if Submit.objects.filter(survey_id=survey, username=username,
#                                  submit_time__gte=datetime.datetime.today().date()):
#             response = {'status_code': 999, 'message': '当天已填写'}
#             return JsonResponse(response)
#
#         if not survey.is_released:
#             return JsonResponse({'status_code': 4, 'message': '问卷未发布'})
#
#         survey.recycling_num = survey.recycling_num + 1
#         survey.save()
#
#         submit = Submit(username=username, survey_id=survey, score=0)
#         submit.save()
#         for answer_dict in answer_list:
#             question = Question.objects.get(question_id=answer_dict['question_id'])
#             answer = Answer(answer=answer_dict['answer'], username=username,
#                             type=answer_dict['type'], question_id=question, submit_id=submit)
#             answer.save()
#
#         return JsonResponse(response)
#
#     else:
#         response = {'status_code': -2, 'message': '请求错误'}
#         return JsonResponse(response)