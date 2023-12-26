from django.contrib import admin

from api.v1.languages.models import Language

admin.ModelAdmin.list_per_page = 50

CUSTOM_ADMIN_ORDERING = [
    ('chapters', ['Chapter']),
    ('lessons', ['Lesson', 'LessonDetail', 'LessonSource', 'LessonWordInfo']),
    ('books', ['Book', 'BookChapter']),
    ('todos', ['Todo']),
    ('questions', ['Question', 'QuestionDetail', 'Category']),
    ('tariffs', ['Tariff']),
    ('discounts', ['TariffDiscount', 'UserCodeDiscount']),
    ('payments', ['Order']),
    ('swish', ['MinBonusMoney', 'SwishCard']),
    ('accounts', ['CustomUser']),
    ('languages', ['Language']),
]


def custom_app_list(self, request):
    app_dict = self._build_app_dict(request)
    lst = []
    for app_name, object_list in CUSTOM_ADMIN_ORDERING:
        app = app_dict[app_name]
        app['models'].sort(key=lambda x: object_list.index(x['object_name']))
        lst.append(app)
    return lst


# admin.AdminSite.get_app_list = custom_app_list


class AbstractStackedInline(admin.StackedInline):
    verbose_name = 'detail'
    verbose_name_plural = 'details'

    def get_languages_count(self):
        return len(Language.get_languages())

    def get_min_num(self, request, obj=None, **kwargs):
        return self.get_languages_count()

    def get_max_num(self, request, obj=None, **kwargs):
        return self.get_languages_count()

    def get_extra(self, request, obj=None, **kwargs):
        return self.get_languages_count() - 1
