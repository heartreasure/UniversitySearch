from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id=request.user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            id = request.user.id
            kwargs["queryset"] = MyUser.objects.filter(id=id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ArticleInfo)
class ArticleInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'articlephoto', 'created', 'updated', 'article_tag', 'user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id=request.user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            id = request.user.id
            kwargs["queryset"] = MyUser.objects.filter(id=id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CollectionInfo)
class CollectionInfoAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'category', 'image', 'description', 'user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id=request.user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            id = request.user.id
            kwargs["queryset"] = MyUser.objects.filter(id=id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
