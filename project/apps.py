from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.module_loading import autodiscover_modules

class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'

def start_celery_beat(sender, **kwargs):
    from django.core import management
    management.call_command('startcelerybeat')

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'

    def ready(self):
        autodiscover_modules('management')
        post_migrate.connect(start_celery_beat, sender=self)