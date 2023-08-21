import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'delete-expire-orders-every-12-minutes': {
        'task': 'api.v1.payments.tasks.delete_expire_orders',
        'schedule': crontab(minute=12)
    },
    'delete-not-confirmed-accounts-every-30-minutes': {
        'task': 'api.v1.accounts.tasks.delete_not_confirmed_accounts',
        'schedule': crontab(minute=30)
    }
}
