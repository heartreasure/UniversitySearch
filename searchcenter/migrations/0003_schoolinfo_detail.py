# Generated by Django 2.2.12 on 2020-04-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchcenter', '0002_schoolinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolinfo',
            name='detail',
            field=models.CharField(default='暂无信息', max_length=100, verbose_name='详细地址'),
        ),
    ]
