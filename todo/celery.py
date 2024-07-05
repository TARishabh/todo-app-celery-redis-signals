from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# from django_celery_beat.models import PeriodicTask

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('todo')

app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
# app.conf.beat_schedule = {
#     'send_mail_everyday_at_8':{
#         'task': 'send_mail_app.tasks.send_mail_task',
#         'schedule': crontab(hour=14, minute=5),
#         # 'args': (2), # you can use this argument in the task function using data keyword
#     }
# }

app.autodiscover_tasks()

@app.task(bind=True)

def debug_task(self):
    print(f'Request: {self.request!r}')