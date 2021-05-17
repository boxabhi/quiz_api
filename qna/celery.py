
from celery import Celery
import os
from celery.schedules import crontab
from datetime import datetime, timedelta
from django.conf import settings
from celery.decorators import periodic_task

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qna.settings')

app = Celery('qna')

app.config_from_object('django.conf:settings', namespace='CELERY')



# @app.task(name="hello_world",bind=True)
# def hello_world():
#     print('Hello World')
    


    
app.conf.beat_schedule = {
    'add-every-40-seconds': {
        'task': 'delete_users',
        'schedule': crontab(minute="*/1"),  
    },
}

#app.autodiscover_tasks(settings.INSTALLED_APPS)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
    
