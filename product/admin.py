from django.contrib import admin
from product.models import Product
from apitest.models import Apis,Apitest
from apitest.admin import ApitestAdmin
from apptest.models import Appcase
from webtest.models import Webcase

# Register your models here.
class ApitestAdmin(admin.TabularInline):
    list_display = ['apitestname', 'apitester','apitestresult','create_time','id','product']
    model = Apitest
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc','create_time','id']
    inlines = [ApitestAdmin]


class ApisAdmin(admin.TabularInline):
    list_display = ['apiname','apiurl','apiparamvalue','apimethod','apiresult','apistatus','create_time','id','product']
    model = Apis
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc','create_time','id']
    inlines = [ApisAdmin]

class AppcaseAdmin(admin.TabularInline):
    list_display = ['appcasename', 'apptestresult','create_time','id','product']
    model = Appcase
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc','create_time','id']
    inlines = [AppcaseAdmin]

class WebcaseAdmin(admin.TabularInline):
    list_display = ['webcasename', 'webtestresult','create_time','id','product']
    model = Webcase
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc','producter','create_time','id']
    inlines = [WebcaseAdmin]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname','productdesc','producter','create_time','id']
admin.site.register(Product) #把产品模块注册到Django admin后台 并能显示