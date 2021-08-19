from django.conf import settings
from userInfo.models import *

from utils.toHash import *

import datetime


def make_confirm_string(user):  # generate confirm_code for user (username+c_time)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code


def send_email_confirm(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.zewan.top的注册确认邮件'

    text_content = '''感谢注册www.zewan.com，这里是网上出版系统，专注于管理出版与审核！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="{}/confirm/?code={}" target=blank>www.zewan.top</a>，\
                    这里是网上出版系统，专注于管理出版与审核！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(settings.WEB_FRONT, code, settings.CONFIRM_DAYS)   # url must be corrected

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
