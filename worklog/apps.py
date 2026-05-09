from django.apps import AppConfig


class WorklogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'worklog'

    def ready(self):
        import worklog.signals
