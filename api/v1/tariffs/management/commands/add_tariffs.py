from django.core.management.base import BaseCommand

from api.v1.tariffs.models import Tariff


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 7):
            Tariff.objects.create(days=i * 10, price=i * 100)
