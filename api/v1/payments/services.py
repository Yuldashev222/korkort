from datetime import timedelta
from django.utils.timezone import now
from api.v1.payments.models import Order


def delete_expire_orders():
    Order.objects.filter(created_at__lt=now() - timedelta(days=1), is_paid=False).delete()
