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


@csrf_exempt
@transaction.atomic
# 事务处理，加悲观锁，并模拟数据库回滚操作
def save_signup_answer_by_code(request):
    response = {'status_code': 1, 'message': 'success'}
    if request.method == 'POST':
        print("问卷提交中...")
        req = json.loads(request.body)
        code = req['code']
        answer_list = req['answers']
        print(req['answers'])
        username = request.session.get('username')
        if username is None:
            username = ''
        print("username"+username)
        survey = Survey.objects.get(share_url=code)
        qn_id = survey.survey_id
        if survey.is_deleted:
            response = {'status_code': 2, 'message': '问卷已删除'}
            return JsonResponse(response)

            # if time.mktime(survey.finished_time.timetuple()) < time.time():
            #     return JsonResponse({'status_code': -1, 'message': '超过截止时间'})

        if Submit.objects.filter(survey_id=survey, username=username) and username != '':#TODO delete
            return JsonResponse({'status_code': 21, 'message': '已提交过问卷'})

        if not survey.is_released:
            return JsonResponse({'status_code': 4, 'message': '问卷未发布'})

        if survey.recycling_num >= survey.max_recycling & survey.max_recycling != 0:
            finish_qn(qn_id)
            return JsonResponse({'status_code': 5, 'message': '人数已满'})
        try:
            with transaction.atomic():
                survey_lock = Survey.objects.select_for_update().get(survey_id=survey.survey_id)
                if survey_lock.recycling_num + 1 > survey_lock.max_recycling:
                    raise SubmitRecyleNumError(survey.recycling_num)
                survey_lock.recycling_num = survey_lock.recycling_num + 1

                survey_lock.save()
                # print("lock_回收数目"+survey_lock.recycling_num)
            # transaction.commit()

        except SubmitRecyleNumError as e:
            print('问卷报名已满,错误信息为',e)
            finish_qn(qn_id)

            return JsonResponse({'status_code': 11, 'message': '问卷报名已满'})
        # transaction.commit()
        question_list = Question.objects.filter(survey_id=survey)
        submit = Submit(username=username, survey_id=survey, score=0)
        submit.save()
        for answer_dict in answer_list:
            if answer_dict['ans'] is None:
                print("answer is None, not save")
                continue
            question = Question.objects.get(question_id=answer_dict['question_id'])
            answer = Answer(answer=answer_dict['answer'], username=username,
                            type=answer_dict['type'], question_id=question, submit_id=submit)
            if answer.answer == '' or answer.answer is None:
                answer.answer = ''
            answer.save()

            if question.type in ["radio", "checkbox"]:
                options = Option.objects.filter(question_id=question)
                from Submit.views import KEY_STR
                print(answer_dict)

                option_content_list = answer_dict['answer'].split(KEY_STR)
                for option in options:

                    print(option.content)
                    if not option.has_num_limit:
                        continue
                    # option = Option.objects.select_for_update().get(option_id=option_not_lock.option_id)
                    if option.content in option_content_list:
                        try:
                            with transaction.atomic():
                                option_lock = Option.objects.select_for_update().get(option_id=option.option_id)
                                if option_lock.remain_num <= 0:
                                    raise OptionRecyleNumError(option_lock.num_limit)

                            option_lock.remain_num -=  1
                            option_lock.save()
                        except OptionRecyleNumError as e:
                            print('问卷存在报名项目报名已满,错误信息为', e)
                            # print("before recycling_num")

                            print("after recycling_num")
                            answer_list = Answer.objects.filter(submit_id=submit)
                            is_stop = False
                            for answer in answer_list:
                                if is_stop:
                                    break
                                question_back = answer.question_id
                                options_rollback = Option.objects.filter(question_id=question_back)
                                for option_roolback in options_rollback:
                                    answer_answer_list = answer.answer.split(KEY_STR)
                                    if option_roolback.content in answer_answer_list and option_roolback.has_num_limit and option_roolback.option_id != option.option_id:
                                        option_roolback.remain_num += 1
                                        # print(answer.answer)
                                        # print(option_roolback.content+"roolback")
                                        option_roolback.save()
                                    elif answer.answer.find(option_roolback.content) >= 0 and option_roolback.has_num_limit and option_roolback.option_id == option.option_id:
                                        # print(option_roolback.content+"not roolback")
                                        is_stop = True
                                        break
                            survey.save()
                            submit.delete()
                            return JsonResponse({'status_code': 12, 'message': '有选项报名已满'})

            answer.save()
        survey.recycling_num = survey.recycling_num + 1
        survey.save()
        return JsonResponse(response)

    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)

