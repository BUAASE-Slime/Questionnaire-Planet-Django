from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    user_desc = models.CharField(max_length=500, blank=True)

    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ": " + self.code

    class Meta:
        db_table = 'tb_confirmCode'
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = verbose_name
