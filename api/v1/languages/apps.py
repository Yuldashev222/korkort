from django.apps import AppConfig


class LanguagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.languages'

    def ready(self):
        from . import signals
