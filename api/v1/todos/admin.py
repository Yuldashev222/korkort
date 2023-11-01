from django.contrib import admin

from api.v1.todos.models import Todo, TodoDetail
from api.v1.general.admin import AbstractStackedInline


class TodoDetailInline(AbstractStackedInline):
    model = TodoDetail


@admin.register(Todo)
class TodoDetailAdmin(admin.ModelAdmin):
    inlines = (TodoDetailInline,)
