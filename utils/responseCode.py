"""
枚举类：定义状态码，用于前后端传输
"""

SUCCESS = '2000'
DEFAULT = '2001'  # 没发送请求或发送请求类型不对
FORM_ERROR = '3001'  # 表单信息错误（未全部填写或数据类型有误）

# 系统错误
PAGE_NOT_FOUND = '404'


# Wrong
class LoginStatus:
    LOGIN_REPEATED = '4001'  # 用户已登录
    USERNAME_MISS = '4002'  # 用户名不存在
    PASSWORD_ERROR = '4003'  # 密码错误
    USER_NOT_CONFIRM = '4004'  # 用户未通过邮件确认


class RegisterStatus:
    USERNAME_REPEATED = '4001'  # 用户名已存在
    EMAIL_ERROR = '4002'  # 邮箱已注册或不可用
    PASSWORD_INVALID = '4003'  # 密码不符合规则，应至少同时包含字母和数字，且长度为 8-18
    PASSWORD_CONTRAST = '4004'  # 两次输入的密码不同
    SEND_EMAIL_ERROR = '4005'  # 邮件验证码发送失败


class LogoutStatus:
    USER_NOT_LOGIN = '4001'  # 用户未登录


class ConfirmStatus:
    STRING_MISS = '4001'  # 验证码不存在，即返回无效的确认请求
    CONFIRM_EXPIRED = '4002'  # 验证码已过期，请重新注册


class VerifyStatus:
    USER_NOT_LOGIN = '4001'  # 用户未登录
    CONFIRM_REPEATED = '4002'  # 用户已验证，无需重复验证
    SEND_EMAIL_ERROR = '4003'  # 邮件发送失败


class UserInfoStatus:
    USER_SELF = '2001'
    USER_MISS = '4001'


class WriterStatus:
    EMAIL_NOT_CONFIRMED = '4001'  # 邮箱未验证
    MESSAGE_NOT_EXIST = '4002'  # 信息不完善
    WRITER_EXIST = '4003'  # 已经申请为作者
    USER_NOT_LOGIN = '4004'
    USER_NOT_EXIST = '4005'


class EditorStatus:
    EMAIL_NOT_CONFIRMED = '4001'  # 邮箱未验证
    MESSAGE_NOT_EXIST = '4002'  # 信息不完善
    Editor_EXIST = '4003'  # 已经申请为编辑
    USER_NOT_LOGIN = '4004'
    USER_NOT_EXIST = '4005'
    ADD_REVIEW_ERROR = '4006'  # 添加审稿人失败


class ArticleStatus:
    UPLOAD_FAILURE = '4001'  # 上传失败
    ARTICLE_NOT_EXIST = '4002'  # 文章不存在


class RemarkStatus:
    REMARK_EXIST = '4001'  # 已提交评论
    REVIEW_NOT_MATCH = '4002'  # 审稿人不能评论该文章
    AR_NOT_EXIST = '4003'  # 不存在审稿人或文章


class WritingPageStatus:
    USER_NOT_LOGIN = '4001'
    USER_NOT_AUTHOR = '4002'
    USER_NOT_EDITOR = '4003'


class GetSessionStatus:
    USER_NOT_LOGIN = '4001'


class EditDetailInfo:
    USER_NOT_LOGIN = '4001'
    USER_NOT_EXIST = '4002'


class FinishMesStatus:
    MES_NOT_FOUND = '4001'


class MesStatus:
    USER_NOT_LOGIN = '4001'
    USER_NOT_EXISTS = '4002'
    NEWS_NOT_EXISTS = '4003'
