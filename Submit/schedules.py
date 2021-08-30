import os, sys, time, datetime
import threading
import django
from django.http import JsonResponse

from Qn.models import Survey

base_apth = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(base_apth)
# 将项目路径加入到系统path中，这样在导入模型等模块时就不会报模块找不到了

# 定时更新数据库信息,不过维护数据较好的话不必使用
sys.path.append(base_apth)
os.environ['DJANGO_SETTINGS_MODULE'] ='djangoProject.settings' # 注意：django_api 是我的模块名，你在使用时需要跟换为你的模块
django.setup()
def confdict_handle():
    while True:
        try:
            loca_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            qn_list = Survey.objects.all()
            for qn in qn_list:
                if qn.finished_time:
                    qn.finished_time = qn.finished_time + datetime.timedelta(minutes=1)
                    qn.save()
            print(loca_time)
            time.sleep(5)

        except Exception as e:
            print('发生错误，错误信息为：', e)
            continue



def timing_task(request):
    '''
    主函数，用于启动所有定时任务，因为当前定时任务是手动实现，因此可以自由发挥
    '''
    try:
        # 启动定时任务，多个任务时，使用多线程
        task1 = threading.Thread(target=confdict_handle)
        task1.start()
    except Exception as e:
        print('发生异常：%s' % str(e))

    return JsonResponse({'status_code':1})
# if __name__ == '__main__':
#     timing_task()
