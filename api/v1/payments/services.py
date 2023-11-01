from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from api.v1.payments.models import Order


def delete_expire_orders():
    Order.objects.filter(created_at__lt=now() - timedelta(minutes=settings.STRIPE_CHECKOUT_TIMEOUT + 1), is_paid=False
                         ).delete()
