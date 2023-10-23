from django.apps import AppConfig


class LevelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.levels'

    def ready(self):
        from . import signals
