import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infolabs.settings')

celery_app = Celery('infolabs')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))