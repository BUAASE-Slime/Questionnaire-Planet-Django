# Generated by Django 3.0 on 2021-08-27 16:45

import Qn.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Qn', '0007_auto_20210826_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='image_url',
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to=Qn.models.question_image_directory_path, verbose_name='图片文件'),
        ),
    ]
