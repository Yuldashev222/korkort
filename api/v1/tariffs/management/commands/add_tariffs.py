from django.core.management.base import BaseCommand

from api.v1.general.enums import title, desc
from api.v1.languages.models import Language
from api.v1.tariffs.models import Tariff, TariffDetail


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 7):
            obj = Tariff.objects.create(days=i * 10, price=i * 100)

            for language in Language.objects.all():
                TariffDetail.objects.create(tariff=obj, language=language, title=title, desc=desc)
