from __future__ import absolute_import
import os
import django
from celery import Celery   #一个简单、灵活和可靠的分布式任务处理系统。专注实时任务队列，也支持任务调度。
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autotest.settings')
django.setup()

app = Celery('autotest')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
