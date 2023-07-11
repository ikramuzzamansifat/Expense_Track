from calendar import monthrange
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render
from rest_framework import generics
from django.views.generic import TemplateView

from api.models import Expense
from api.serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token

from .tasks import test_func
from send_mail_app.tasks import send_mail_func, send_report_func
import json
from datetime import date, datetime
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.shortcuts import redirect


def test(request):
    test_func.delay()
    return HttpResponse("Hi, Done")


def send_mail_to_all(request):
    send_mail_func.delay()

    return HttpResponse("Sent Mail")


def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour=10, minute=42)
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name="schedule_mail_task" + "4",
        task="send_mail_app.tasks.send_mail_func",
        # task="send_mail_app.tasks.send_report_func",
    )  # , args = json.dumps())
    return HttpResponse("Sent scheduled mail")


class CompositeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def send_report_range(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    expenses_within_range = Expense.objects.filter(
        date__range=(start_date, end_date)
    ).values()
    expenses_list = list(expenses_within_range)

    json_response = json.dumps(expenses_list, cls=CompositeEncoder)

    # Call the Celery task asynchronously
    send_report_func.delay(json_response)

    return JsonResponse("String " + json_response, safe=False)


def schedule_report_mail(request):
    # Create or get the CrontabSchedule for the desired time (e.g., 10:42 AM)

    schedule, created = CrontabSchedule.objects.get_or_create(hour=11, minute=34)
    # Create a PeriodicTask for the schedule
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name="schedule_mail_task" + str(datetime.now()),
        task="send_mail_app.tasks.send_mail_func",
    )

    return redirect(
        "/schedule-report-range/"
    )  # Redirect to the schedule_report_range view


def schedule_report_range(request):
    current_date = datetime.now().date()

    # Calculate the previous month's start and end dates
    if current_date.month == 1:
        previous_month_year = current_date.year - 1
        previous_month = 12
    else:
        previous_month_year = current_date.year
        previous_month = current_date.month - 1

    start_date = date(previous_month_year, previous_month, 1)

    _, last_day = monthrange(previous_month_year, previous_month)
    end_date = date(previous_month_year, previous_month, last_day)

    # Print the start_date and end_date
    print(start_date)  # Output: 2023-06-01
    print(end_date)  # Output: 2023-06-30

    expenses_within_range = Expense.objects.filter(
        date__range=(start_date, end_date)
    ).values()
    expenses_list = list(expenses_within_range)

    json_response = json.dumps(expenses_list, cls=CompositeEncoder)

    # Call the Celery task asynchronously
    send_report_func.delay(json_response)

    return HttpResponse("Sent Report rangess...")
    # return HttpResponse(json_response)


def send_report(request):
    json_report = json.loads(request.body)
    print(json_report)
    send_report_func.delay(json_report)
    response = {"response": "Sending Main..."}
    response = json.dumps(response)
    return HttpResponse(response, content_type="application/json")


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseHistoryView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.all()


class ExpenseHistoryIdView(APIView):
    def get(self, request, pk):
        object = Expense.objects.filter(id=pk).first()
        if not object:
            return Response({"message": "Value with this id not found"})
        serializer = ExpenseSerializer(object)
        return Response(serializer.data)


class ExpenseHistoryWithDateView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        date = self.kwargs.get("date")
        return Expense.objects.filter(date=date)


# For Frontend


class CreateExpense(TemplateView):
    template_name = "expense_create.html"


class IndexView(TemplateView):
    template_name = "index.html"


class HistoryView(TemplateView):
    template_name = "history.html"


class HistoryDateView(TemplateView):
    template_name = "history_date.html"


class TotalExpenseWithDateView(APIView):
    def get(self, request, date):
        # date = self.kwargs.get("date")
        total_expense = Expense.objects.filter(date=date).aggregate(total=Sum("amount"))
        total_amount = total_expense["total"] or 0

        return Response({"total_expense": total_amount})


class HistoryReportView(TemplateView):
    template_name = "history_report.html"
