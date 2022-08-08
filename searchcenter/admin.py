from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'school_url', 'is_build', 'area', 'detail', 'user']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id=request.user.id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            id = request.user.id
            kwargs["queryset"] = MyUser.objects.filter(id=id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'tf_idf']


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'count', 'created', 'updated']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_list']


@admin.register(CntToUrl)
class CntToUrlAdmin(admin.ModelAdmin):
    list_display = ['cnt', 'title', 'url', 'school']
    list_display_links = ['cnt', 'title']


@admin.register(WordToCnt)
class WordToCntAdmin(admin.ModelAdmin):
    list_display = ['word', 'cnt_list', 'school']