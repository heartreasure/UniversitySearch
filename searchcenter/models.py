from django.db import models

# Create your models here.
from django.utils import timezone

from index.models import MyUser


class SchoolInfo(models.Model):
    # id，学校名称，URL，是否已经建立词库，所属地区
    id = models.AutoField(primary_key=True)
    school_name = models.CharField('高校名称', max_length=50, blank=False)
    school_url = models.CharField('高校URL地址', max_length=100, blank=False)
    is_build = models.BooleanField('是否已经建立词库', default=False)
    area = models.CharField('所属地区', max_length=100)
    detail = models.CharField('详细地址', max_length=100, default='暂无信息')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户', default=9)

    def __str__(self):
        return self.school_name

    class Meta:
        verbose_name = '高校信息'
        verbose_name_plural = '高校信息'


class CntToUrl(models.Model):
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, verbose_name='学校')
    cnt = models.IntegerField('子网页序号')
    url = models.CharField('子网页URL', max_length=100)
    title = models.CharField('子网页标题', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '网页序号和URL'
        verbose_name_plural = '网页序号和URL'


class WordToCnt(models.Model):
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE, verbose_name='学校')
    word = models.CharField('单词', max_length=100)
    cnt_list = models.TextField('网页列表')

    def __str__(self):
        return self.cnt_list

    class Meta:
        verbose_name = '单词和网页'
        verbose_name_plural = '单词和网页'


class SearchResult(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField('网址', max_length=100)
    title = models.CharField('标题', max_length=200)
    tf_idf = models.FloatField('TF-IDF')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '搜索结果'
        verbose_name_plural = '搜索结果'


class SearchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=200)
    url = models.CharField('网址', max_length=200)
    count = models.IntegerField('访问次数')
    created = models.DateTimeField('创建时间', default=timezone.now)
    updated = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '历史记录'
        verbose_name_plural = '历史记录'


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField('分类', max_length=100)
    category_list = models.CharField('搜索字段', max_length=200)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = '分类检索'
        verbose_name_plural = '分类检索'


