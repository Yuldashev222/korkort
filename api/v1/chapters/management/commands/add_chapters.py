from uuid import uuid4
from django.core.management.base import BaseCommand

from api.v1.chapters.models import Chapter


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(20):
            Chapter.objects.create(title_swe=f'{uuid4()}',
                                   title_en=f'{uuid4()}',
                                   title_e_swe=f'{uuid4()}',
                                   desc_swe=f'{uuid4()} {uuid4()}',
                                   desc_en=f'{uuid4()} {uuid4()}',
                                   desc_e_swe=f'{uuid4()} {uuid4()}',
                                   image=f'Screenshot_from_2023_20-41-00.png',
                                   ordering_number=i + 1)
