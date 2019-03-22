from django.contrib import admin
from apitest.models import Apitest, Apistep,Apis
from product.models import Product
# Register your models here.
class ApistepAdmin(admin.TabularInline):
    list_display = ['apiname', 'apiurl','apiparamvalue','apimethod','apiresult','apistatus','create_time','id','apitest']
    model = Apistep
    extra = 1

class ApitestAdmin(admin.ModelAdmin):
    list_display = ['apitestname','apitester','apitestresult','create_time','id']
    inlines = [ApistepAdmin]


class ApisAdmin(admin.TabularInline):
    list_display = ['apiname','apiurl','apiparamvalue','apimethod','apiresult','apistatus','create_time','id','product']

admin.site.register(Apitest, ApitestAdmin)
admin.site.register(Apis)



# admin.site.register(ApisAdmin)

#admin.site.register([Apitest, ApistepAdmin])