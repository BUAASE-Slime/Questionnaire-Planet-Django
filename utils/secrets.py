
class Secrets:
    class Email:
        emailHost = 'smtp.126.com'
        emailPort = 25
        emailAddr = 'zewancc@126.com'
        emailPasswd = 'IFFYHIMFEDLICRUO'  # 邮箱 SMTP 授权码，此处为虚拟，须修改

    class DataBase:
        # database information

        host = '82.156.217.192'
        user = 'root'
        passwd = 'BUAASE43'  # 修改为您本地或远程的 mysql数据库信息
        db = 'pt'

    class Host:  # 修改为django允许运行的网址
        allowedHost = ['localhost', '127.0.0.1', 'zewan.cc']

    class RootUrl:
        webFront = 'http://127.0.0.1:8080'
        webBack = 'https://zewan.cc/api/qs'
