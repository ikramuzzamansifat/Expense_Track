from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_tracker.settings")

app = Celery("expense_tracker")
app.conf.enable_utc = False

app.conf.update(timezone="Asia/Dhaka")

app.config_from_object(settings, namespace="CELERY")

# Celery beat settings ( time / interval)
app.conf.beat_schedule = {
    "send-mail-every-day-at-8": {
        "task": "send_mail_app.tasks.send_report_func",
        "schedule": crontab(hour=19, minute=29),  # day_of_month=19, month_of_year
        #         # "args": (2,),
    }
}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request|r}")
