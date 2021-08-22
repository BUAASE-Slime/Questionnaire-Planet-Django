# Generated by Django 3.0 on 2021-08-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Qn', '0003_auto_20210822_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='docx_url',
            field=models.URLField(default='', verbose_name='word链接'),
        ),
        migrations.AddField(
            model_name='survey',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='是否已结束'),
        ),
        migrations.AddField(
            model_name='survey',
            name='pdf_url',
            field=models.URLField(default='', verbose_name='pdf链接'),
        ),
    ]