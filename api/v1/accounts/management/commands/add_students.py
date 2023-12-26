from uuid import uuid4
from django.core.management.base import BaseCommand

from api.v1.accounts.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(100):
            self.stdout.write(str(i))
            CustomUser.objects.create_user(name=f'Student No {i}',
                                           password='123123asdasd',
                                           email=str(uuid4()) + '@gmail.com',
                                           is_verified=False,
                                           is_staff=False)
