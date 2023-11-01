from django.apps import AppConfig


class TodosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.todos'

    def ready(self):
        from . import signals
