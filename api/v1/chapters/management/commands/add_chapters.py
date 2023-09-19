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
                                   image=f'chapters/1%3A%20a940a76e-290f-46c7-ac6d-0a3/lessons/1%3A%2014303787-0823-44c8-a572-535/images/Re_hDa0ivt.png',
                                   ordering_number=i + 1)
