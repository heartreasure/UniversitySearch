from django.db import models
from django.utils import timezone
from index.models import MyUser
# from ckeditor_uploader.fields import RichTextUploadingField
from tinymce.models import HTMLField


class ArticleTag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField('分类标签', max_length=50)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = '分类标签'
        verbose_name_plural = '分类标签'


class ArticleInfo(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户')
    author = models.CharField('作者', max_length=50, default='Ancientear')
    title = models.CharField('文章标题', max_length=200, default='暂无标题')
    abstract = models.TextField('摘要', default='暂无摘要')
    content = HTMLField(verbose_name='文章内容', default='暂无内容')
    articlephoto = models.ImageField('文章图片', blank=True, upload_to='images/article/')
    created = models.DateTimeField('创建时间', default=timezone.now)
    updated = models.DateTimeField('更新时间', auto_now=True)
    article_tag = models.ForeignKey(ArticleTag, on_delete=models.CASCADE, verbose_name='分类标签')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '动态内容'
        verbose_name_plural = '动态内容'


# 收藏类
class CollectionInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='用户')
    image_name = models.CharField('图片名称', max_length=50, default='暂无名称')
    category = models.CharField('图片分类', max_length=10)
    image = models.ImageField('图片', blank=True, upload_to='images/collection/')
    description = models.CharField('图片描述', max_length=200, default='暂无描述')

    def __str__(self):
        return self.image_name

    class Meta:
        verbose_name = '图片收藏'
        verbose_name_plural = '图片收藏'
