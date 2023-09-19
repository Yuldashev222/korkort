from uuid import uuid4

from django.core.management.base import BaseCommand

from api.v1.discounts.models import StudentDiscount, TariffDiscount
from api.v1.tariffs.models import Tariff


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not StudentDiscount.objects.exists():
            StudentDiscount.objects.create(title=f'{str(uuid4())}', discount_value=2, is_percent=True)

        if not TariffDiscount.objects.exists():
            TariffDiscount.objects.create(title=f'{str(uuid4())}', discount_value=20, is_percent=True,
                                          image='chapters/1%3A%20a940a76e-290f-46c7-ac6d-0a3/lessons/1%3A%2014303787-0823-44c8-a572-535/images/Re_hDa0ivt.png')
        for i in range(1, 7):
            Tariff.objects.create(title=f'{str(uuid4())}', desc=f'{str(uuid4())} {str(uuid4())}', days=i * 10,
                                  price=i * 100, tariff_discount=i % 2 == 0, student_discount=i % 2 == 1)
