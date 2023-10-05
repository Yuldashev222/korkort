from datetime import timedelta
from django.utils.timezone import now

from api.v1.accounts.models import CustomUser


def delete_not_confirmed_accounts():
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(days=1), is_staff=False, is_verified=False).delete()
