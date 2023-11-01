from django.core.management.base import BaseCommand
from api.v1.languages.models import Language


class Command(BaseCommand):
    def handle(self, *args, **options):
        for idx, i in enumerate(['sweden', 'russian', 'uzbek', 'english', 'czech', 'latvian', 'arabic'], 1):
            Language.objects.create(name=i, ordering_number=idx)
