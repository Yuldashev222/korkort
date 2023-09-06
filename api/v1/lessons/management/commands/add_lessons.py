from django.core.management.base import BaseCommand

from api.v1.lessons.tasks import create_lessons


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_lessons.delay()
