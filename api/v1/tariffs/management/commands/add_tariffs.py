from uuid import uuid4

from django.core.management.base import BaseCommand

from api.v1.discounts.models import StudentDiscount, TariffDiscount
from api.v1.tariffs.models import Tariff


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not StudentDiscount.objects.exists():
            StudentDiscount.objects.create(
                title=f'{str(uuid4())} {str(uuid4())} {str(uuid4())} {str(uuid4())} {str(uuid4())}',
                discount_value=2,
                is_percent=True,
            )
        if not TariffDiscount.objects.exists():
            TariffDiscount.objects.create(
                title=f'{str(uuid4())} {str(uuid4())} {str(uuid4())} {str(uuid4())} {str(uuid4())}',
                discount_value=20,
                is_percent=True,
                image='Screenshot_from_2023-08-17_20-41-00_G2TBmpL.png'
            )
        for i in range(7):
            Tariff.objects.create(title=f'{str(uuid4())} {str(uuid4())}',
                                  desc=f'{str(uuid4())} {str(uuid4())} {str(uuid4())} {str(uuid4())} {str(uuid4())}',
                                  days=i * 10,
                                  price=i * 100,
                                  tariff_discount=i % 2 == 0,
                                  student_discount=i % 2 == 1)
