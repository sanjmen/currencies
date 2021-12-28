import os
import environ

from celery import Celery

from django.apps import apps, AppConfig
from django.conf import settings

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env("config/settings/.env")  # reading .env file

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.common")  # pragma: no cover


app = Celery("taskapp")



class TaskappConfig(AppConfig):
    name = "apps.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        app.config_from_object("django.conf:settings", namespace="CELERY")
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from apps.markets.tasks import update_markets, update_klines

    sender.add_periodic_task(settings.UPDATE_MARKETS_INTERVAL, update_markets.s())
    sender.add_periodic_task(settings.UPDATE_KLINES_INTERVAL, update_klines.s())

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))