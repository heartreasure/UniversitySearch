from django.contrib import admin
from .models import MyUser, FeedbackInfo
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
# Register your models here.


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email',
                    'name', 'telephone', 'introduce', 'address', 'photo']
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = (_('Personal info'),
                    {'fields': ('email', 'name', 'telephone', 'introduce', 'address', 'photo')})

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(id=request.user.id)


@admin.register(FeedbackInfo)
class FeedbackInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'type', 'info']


admin.site.site_title = '高校门户网站检索系统后台管理'
admin.site.site_header = '高校门户网站检索系统'

