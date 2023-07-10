from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from expense_tracker import settings


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = "if you are liking, don't hit the like button"
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Sent Mail Done"


@shared_task(bind=True)
def send_report_func(self, json_report):
    users = get_user_model().objects.all()
    print(json_report)
    json_report = f"{json_report}"
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = json_report
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Sent Mail Done"
