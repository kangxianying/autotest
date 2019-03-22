from django.contrib import admin

# Register your models here.
from django.contrib import admin
from set.models import Set

class SetAdmin(admin.ModelAdmin):
    list_display = ['setname','setvalue','id']

admin.site.register(Set) # 把系统设置模块注册到django admin后台并能显示