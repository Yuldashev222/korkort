from django.core.management.base import BaseCommand

from api.v1.accounts.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(100):
            CustomUser.objects.create_user(
                password='123123asdasd',
                first_name=f'Student No {i}',
                last_name=f'Student No {i}',
                bonus_money=i,
                is_verified=True,
                ball=i
            )
