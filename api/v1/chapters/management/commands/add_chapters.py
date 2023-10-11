from django.core.management.base import BaseCommand

from api.v1.chapters.models import Chapter, ChapterDetail
from api.v1.general.enums import title, desc
from api.v1.languages.models import Language


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(20):
            obj = Chapter.objects.create(ordering_number=i + 1,
                                         image='chapters/1:_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')

            for language in Language.objects.all():
                ChapterDetail.objects.create(chapter=obj, language=language, title=title, desc=desc)
