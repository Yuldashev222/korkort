from django.core.management.base import BaseCommand

from api.v1.tariffs.models import Tariff


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 7):
            temp = i % 2 == 1
            Tariff.objects.create(days=i * 10, tariff_discount=temp, student_discount=temp, price=i * 100)
