from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 用户模型类
class MyUser(AbstractUser):
    # 姓名
    name = models.CharField('姓名', max_length=50, default='匿名用户')
    # 联系电话
    telephone = models.CharField('联系电话', max_length=11, default='暂无信息')
    # 简介
    introduce = models.TextField('简介', default='暂无介绍')
    # 地址
    address = models.CharField('住址', max_length=100, default='暂无信息')
    # 头像
    photo = models.ImageField('头像', blank=True, upload_to='images/user/')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户列表'
        verbose_name_plural = '用户列表'


# 反馈信息
class FeedbackInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('姓名', max_length=50, default='匿名用户')
    email = models.EmailField('邮箱', max_length=50, default='暂无信息')
    type = models.CharField('意见类型', max_length=50, default='暂无信息')
    info = models.TextField('反馈信息', default='暂无信息')

    def __str__(self):
        return self.info

    class Meta:
        verbose_name = '反馈信息'
        verbose_name_plural = '反馈信息'
