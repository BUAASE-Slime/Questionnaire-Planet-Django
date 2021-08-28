from django.db import models

# Create your models here.

def image_directory_path(instance, filename):
    # 文件上传到 MEDIA_ROOT/image/question_<id>/<filename>目录中
    return 'image/{0}'.format(filename)


def video_directory_path(instance, filename):
    # 文件上传到 MEDIA_ROOT/image/question_<id>/<filename>目录中
    return 'video/{0}'.format(filename)


class ImageModel(models.Model):
    image_id = models.AutoField(primary_key=True, verbose_name="id")
    instance = models.ImageField(upload_to=image_directory_path, blank=True, default='', verbose_name='图片文件')


class VideoModel(models.Model):
    video_id = models.AutoField(primary_key=True, verbose_name='id')
    instance = models.ImageField(upload_to=video_directory_path, blank=True, default='', verbose_name='视频文件')
