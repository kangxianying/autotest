from django.shortcuts import render
from bug.models import Bug
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login
# Create your views here.

def bug_manage(request):
    username = request.session.get('user','')
    bug_list = Bug.objects.all().order_by('id')
    bug_count = Bug.objects.all().count()
    paginator = Paginator(bug_list,8)
    page = request.GET.get('page',1)
    currentPage = int(page)
    try:
        bug_list = paginator.page(page)
    except PageNotAnInteger:
        bug_list = paginator.page(1)
    except EmptyPage:
        bug_list = paginator.page(paginator.num_pages)
    return render(request, "bug_manage.html", {"user": username,"bugs": bug_list,"bugcounts": bug_count})

@login_required
def bugsearch(request):
    username = request.session.get('user','')
    search_bugname = request.GET.get("bugname","")
    bug_list = Bug.objects.filter(bugname__icontains = search_bugname)
    return render(request, 'bug_manage.html',{"user": username,"bugs":bug_list})