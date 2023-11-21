from django.core.management.base import BaseCommand

from api.v1.books.models import Book, BookChapter
from api.v1.general.enums import title, desc
from api.v1.languages.models import Language


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(20):
            for language in Language.objects.all():
                obj = Book.objects.create(ordering_number=i + 1, language_id=language.pk, title=title)
                for j in range(5):
                    BookChapter.objects.create(book_id=obj.pk, ordering_number=j + 1, is_open=j < 2, title=title,
                                               audio='books/chapters/audios/a.mp3', content=desc)
