from django.apps import AppConfig


class LandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'land'

    def ready(self):
        import land.signals
