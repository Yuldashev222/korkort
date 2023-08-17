from celery import shared_task

from api.v1.payments.models import Order


@shared_task
def delete_expire_orders():
    Order.expire_orders().delete()
