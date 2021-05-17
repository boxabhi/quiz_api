
from celery import Celery
import os
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qna.settings')

app = Celery('qna')

app.config_from_object('django.conf:settings', namespace='CELERY')


    
app.conf.beat_schedule = {
    'add-every-3-minute': {
        'task': 'delete_users',
        'schedule': crontab(minute="*/3"),  
        
    },
}


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
