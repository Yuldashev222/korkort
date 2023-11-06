from django.apps import AppConfig


class ChaptersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.chapters'

    def ready(self):
        from . import signals
