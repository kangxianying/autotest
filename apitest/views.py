from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate,login
from apitest.models import Apitest,Apistep,Apis
import pymysql


# Create your views here.

def home(request):
    return render(request,"home.html")


def login(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home/')
            return response
        else:
            return render(request, 'login.html', {'error':'username or password error'})
    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return render(request,'login.html')



#流程接口管理
@login_required
def apitest_manage(request):
    apitest_list = Apitest.objects.all()  #获取所有接口测试用例
    username = request.session.get('user', '')  # 读取浏览器登录session
    return render(request, "apitest_manage.html", {"user": username,"apitests": apitest_list})

# 接口步聚管理
@login_required
def apistep_manage(request):
    username = request.session.get('user', '')
    # apitestid = request.GET.get('apitest.id',None)
    # apitest = Apitest.objects.get(id=apitestid)      #获取所有接口测试用例
    apistep_list = Apistep.objects.all()
    return render(request, "apistep_manage.html",  {"user": username,"apisteps": apistep_list})

# 单一接口管理
@login_required
def apis_manage(request):
    username = request.session.get('user', '')
    apis_list = Apis.objects.all()
    # apis_count = Apis.objects.all().count()  #统计产品数
    # paginator = Paginator(apis_list, 8)  #生成paginator对象,设置每页显示8条记录
    # page = request.GET.get('page',1)  #获取当前的页码数,默认为第1页
    # currentPage=int(page)  #把获取的当前页码数转换成整数类型
    # try:
    #     apis_list = paginator.page(page)#获取当前页码数的记录列表
    # except PageNotAnInteger:
    #     apis_list = paginator.page(1)#如果输入的页数不是整数则显示第1页的内容
    # except EmptyPage:
    #     apis_list = paginator.page(paginator.num_pages)#如果输入的页数不在系统的页数中则显示最后一页的内容
    return render(request, "apis_manage.html", {"user": username,"apiss": apis_list}) #把值赋给apiscounts这个变量


# 测试报告
@login_required
def test_report(request):
    username = request.session.get('user', '')
    apis_list = Apis.objects.all()
    apis_count = Apis.objects.all().count()  # 统计接口数
    db = pymysql.connect(user='root', db='autotest', passwd='123456', host='127.0.0.1')
    cursor = db.cursor()
    sql1 = 'SELECT count(id) FROM apitest_apis WHERE apitest_apis.apistatus=1'
    aa = cursor.execute(sql1)
    apis_pass_count = [row[0] for row in cursor.fetchmany(aa)][0]
    sql2 = 'SELECT count(id) FROM apitest_apis WHERE apitest_apis.apistatus=0'
    bb = cursor.execute(sql2)
    apis_fail_count = [row[0] for row in cursor.fetchmany(bb)][0]
    db.close()
    return render(request, "report.html",
                  {"user": username, "apiss": apis_list, "apiscounts": apis_count, "apis_pass_counts": apis_pass_count,
                   "apis_fail_counts": apis_fail_count})  # 把值赋给apiscounts这个变量


# 测试报告
@login_required
def apitest_report(request):
    username = request.session.get('user', '')
    return render(request, "apitest_report.html")



