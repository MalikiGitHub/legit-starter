from django.apps import AppConfig


class VtuappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vtuapp'


    def ready(self):
        import vtuapp.signals