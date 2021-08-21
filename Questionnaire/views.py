import pytz
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import BooleanFilter
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from Questionnaire.models import Survey

utc = pytz.UTC

polygon_view_get_desc = '根据所选参数,获取问卷列表,默认按创建时间倒序'
polygon_view_get_parm = [
    Parameter(name='survey_id', in_=IN_QUERY, description='问卷编号', type=TYPE_INTEGER, required=False),
    Parameter(name='is_deleted', in_=IN_QUERY, description='是否删除', type=TYPE_BOOLEAN, required=False),
    Parameter(name='title_key', in_=IN_QUERY, description='标题关键词', type=TYPE_STRING, required=False),
    Parameter(name='username', in_=IN_QUERY, description='发起人用户名', type=TYPE_STRING, required=False),
    Parameter(name='is_released', in_=IN_QUERY, description='是否发布', type=TYPE_BOOLEAN, required=False),
    Parameter(name='is_collected', in_=IN_QUERY, description='是否收藏,', type=TYPE_BOOLEAN, required=False),
    Parameter(name='order_item', in_=IN_QUERY, description='排序项,created_time-创建时间,release_time-发布时间,recycling_num-回收量', type=TYPE_STRING, required=False),
    Parameter(name='order_type', in_=IN_QUERY, description='排序类型,desc-倒序,asc-正序', type=TYPE_STRING, required=False),
]
polygon_view_get_resp = {200: '查询成功', 401: '查询失败'}


@csrf_exempt
@swagger_auto_schema(method='get',
                     tags=['问卷相关'],
                     operation_summary='查询问卷列表',
                     operation_description=polygon_view_get_desc,
                     manual_parameters=polygon_view_get_parm,
                     responses=polygon_view_get_resp
                     )
@api_view(['GET'])
def get_list(request):
    if request.method == 'GET':

        survey_id = request.GET.get('survey_id')
        is_deleted = bool(request.GET.get('is_deleted'))
        title_key = request.GET.get('title_key')
        username = request.GET.get('username')
        is_released = bool(request.GET.get('is_released'))
        is_collected = bool(request.GET.get('is_collected'))
        order_item = request.GET.get('order_item')
        order_type = request.GET.get('order_type')
        if order_item is None:
            order_item = "created_time"
        if order_type is None:
            order_type = "desc"

        if survey_id is not None:
            try:
                survey = Survey.objects.get(survey_id=survey_id)
                json_item = {"survey_id": survey.survey_id, "title": survey.title,
                             "subtitle": survey.subtitle, "is_released": survey.is_released,
                             "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                             "recycling_num": survey.recycling_num, "username": survey.username,
                             "created_time": survey.created_time, "release_time": survey.release_time}
                return JsonResponse(json_item)
            except:
                return JsonResponse({'status_code': 401})

        survey_list = Survey.objects.all()
        if is_deleted:
            survey_list = survey_list.filter(is_deleted=is_deleted)
        if title_key:
            survey_list = survey_list.filter(title__contains=title_key)
        if username:
            survey_list = survey_list.filter(username=username)
        if is_released:
            survey_list = survey_list.filter(is_released=is_released)
        if is_collected:
            survey_list = survey_list.filter(is_collected=is_collected)
        if order_type == 'desc':
            survey_list = survey_list.order_by('-' + order_item)
        else:
            survey_list = survey_list.order_by(order_item)

        json_list = []
        for survey in survey_list:
            json_item = {"survey_id": survey.survey_id, "title": survey.title,
                         "subtitle": survey.subtitle, "is_released": survey.is_released,
                         "is_collected": survey.is_collected, "is_deleted": survey.is_deleted,
                         "recycling_num": survey.recycling_num, "username": survey.username,
                         "created_time": survey.created_time, "release_time": survey.release_time}
            json_list.append(json_item)
        return JsonResponse(list(json_list), safe=False, json_dumps_params={'ensure_ascii': False})
