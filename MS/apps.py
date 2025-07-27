from django.apps import AppConfig


class MsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MS'
    
    def ready(self):
        import MS.signals

            