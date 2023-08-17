from django.apps import AppConfig


class LessonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.lessons'

    def ready(self):
        from . import signals
