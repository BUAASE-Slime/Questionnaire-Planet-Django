from django.db import models
from userinfo.models import *
# Create your models here.

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True,verbose_name="id")
    title = models.CharField(max_length=50,verbose_name="标题")
    subtitle = models.CharField(max_length=256,verbose_name="副标题",blank=True)
    # password = models.CharField(max_length=64,blank=True,)

    question_num = models.PositiveIntegerField(default=0,verbose_name="题目数目") # 非负整数
    recycling_num = models.PositiveIntegerField(default=0,verbose_name="回收数目")

    created_time = models.DateTimeField(auto_now=True,verbose_name="创建时间")
    release_time = models.DateTimeField(blank=True,verbose_name="发布时间")
    finished_time = models.DateTimeField(blank=True,verbose_name="结束时间")

    is_released = models.BooleanField(default=False,verbose_name="是否已发行")
    is_deleted = models.BooleanField(default=False,verbose_name="是否已删除")
    is_collected = models.BooleanField(default=False, verbose_name="是否已收藏")
    # is_encrypted_pin = models.BooleanField(default=False)

    username = models.CharField(max_length=128, unique=True,verbose_name="用户名")

    SURVEY_TYPE_CHOICES = [
        (0,'普通问卷'),
        (1,'考试问卷'),
        (2,'投票问卷'),
        (3,'报名问卷'),
    ]
    type = models.IntegerField(choices=SURVEY_TYPE_CHOICES,default=0,verbose_name="问卷类型")


class Question(models.Model):

    id = models.AutoField(primary_key=True,verbose_name="问题id")
    title = models.CharField(max_length=64,verbose_name="标题")
    direction = models.CharField(max_length=256,blank=True,verbose_name="说明")
    is_must_answer = models.BooleanField(default=False,verbose_name="是必答题")

    survey_id = models.ForeignKey(Survey,on_delete=models.CASCADE,verbose_name="所属问卷id")
    sequence = models.IntegerField(default=0,verbose_name="题目顺序")

    TYPE_CHOICES = [
        (0, '单选'),
        (1, '多选'),
        (2, '填空'),
        (3, '评分'),
    ]
    type = models.IntegerField(choices=TYPE_CHOICES,default=0,verbose_name="题型")

class Option(models.Model):

    id = models.AutoField(primary_key=True,verbose_name="选项编号")
    content = models.CharField(max_length=128,verbose_name="内容")
    question_id  = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name="问题编号")

class Submit(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="提交编号")
    survey_id = models.ForeignKey(Survey,on_delete=models.CASCADE,verbose_name="问卷编号")
    submit_time = models.DateTimeField(auto_now_add=True,verbose_name="提交时间")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="用户编号")

class Answer(models.Model):

    id = models.AutoField(primary_key=True,verbose_name="回答编号")
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name="问题编号")
    submit_id = models.ForeignKey(Submit, on_delete=models.CASCADE,verbose_name="提交编号")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="用户编号")
    answer = models.CharField(max_length=128,verbose_name="答案")
    TYPE_CHOICES = [
        (0, '单选'),
        (1, '多选'),
        (2, '填空'),
        (3, '评分'),
    ]
    type = models.IntegerField(choices=TYPE_CHOICES, default=0,verbose_name="题目类型")

