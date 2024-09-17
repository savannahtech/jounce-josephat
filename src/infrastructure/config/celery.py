import os

from celery import Celery
from celery.schedules import crontab

# Default to every 2 minutes, otherwise once a month
schedule_type = os.getenv("SCHEDULE_TYPE", "default")

if schedule_type == "monthly":
    schedule = crontab(
        minute=0,  # At midnight
        hour=0,  # At the start of the day
        day_of_month=1,  # On the first of every month
        month_of_year="*",
    )
else:
    # Default to run every minute
    schedule = crontab(minute="*")


class CeleryConfig:
    """
    Celery config class
    """

    CELERY_IMPORTS = "src.application.usecases.tasks"
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "Africa/Nairobi"
    CELERY_ENABLE_UTC = False

    CELERYBEAT_SCHEDULE = {
        "src.application.usecases.tasks.refresh_rankings": {
            "args": (),
            "kwargs": {},
            "options": {},
            "relative": False,
            "schedule": schedule,
            "task": "src.application.usecases.tasks.refresh_rankings",
        },
    }


def make_celery(app):
    """
    The function creates a new Celery object, configures it with
    the broker from the application config, updates the
    rest of the Celery config from the Flask
    config and then creates a subclass of the task that
    wraps the task execution in an application context.
    """
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    celery.config_from_object(CeleryConfig)
    return celery
