from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'STORE.settings')

app = Celery('STORE')

# Using a string here means the worker will not have to
# pickle the object when using Windows
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all registered apps
app.autodiscover_tasks()
