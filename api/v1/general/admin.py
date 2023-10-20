from django.contrib import admin

from api.v1.languages.models import Language


class AbstractTabularInline(admin.TabularInline):
    min_num = 1
    max_num = len(Language.get_languages())
    extra = len(Language.get_languages()) - 1
    verbose_name = 'detail'
    verbose_name_plural = 'details'


class AbstractStackedInline(AbstractTabularInline):
    template = "admin/edit_inline/stacked.html"
