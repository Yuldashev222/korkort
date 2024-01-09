from django.core.management.base import BaseCommand
from api.v1.languages.models import Language


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in ['sweden', 'russian', 'uzbek', 'english', 'czech', 'latvian', 'arabic']:
            Language.objects.create(name=i)
