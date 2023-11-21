from django.core.management.base import BaseCommand

from api.v1.todos.models import Todo, TodoDetail
from api.v1.general.enums import title, desc
from api.v1.languages.models import Language


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(40):
            todo = Todo.objects.create(ordering_number=i + 1)
            for language in Language.objects.all():
                TodoDetail.objects.create(todo_id=todo.pk, language_id=language.pk, title=title, text=desc)

