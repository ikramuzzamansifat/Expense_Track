import json
from datetime import date, datetime, timedelta
from calendar import monthrange
from decimal import Decimal


from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.views import View 

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


from api.models import Expense
from api.serializers import ExpenseSerializer
from send_mail_app.tasks import send_mail_func, send_report_func
from .tasks import test_func

# Utility functions 

def get_json_response(data):
    return JsonResponse(data, safe=False)

def get_expenses_within_range(start_date, end_date):
    return Expense.objects.filter(date__range=(start_date, end_date)).values()

def serialize_expenses(expenses):
    return json.dumps(list(expenses), cls=CompositeEncoder)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})



# Views for Expense


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



class CompositeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


# Views for Celery 

class TestView(APIView):
    def get(self, request):
        test_func.delay()
        return Response("Hi, I am done")


class SendMailView(APIView):
    def get(self, request):
        send_mail_func.delay()
        return Response("Mail sent, please check your mail")

class SendReportRangeView(APIView):
    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        print(start_date, end_date)
        expenses_within_range = get_expenses_within_range(start_date, end_date)
        json_response = serialize_expenses(expenses_within_range)

        send_report_func.delay(json_response)
        return get_json_response("String " + json_response)


# Views for Celery Beat

# a schedulemail view such that it will send mail current time + 1 minute
class ScheduleMailView(View):
    def get(self, request):
        current_time = datetime.now()
        scheduled_time = current_time + timedelta(minutes=1)

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=scheduled_time.minute,
            hour=scheduled_time.hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        )
        
        task = PeriodicTask.objects.create(
            crontab=schedule,
            name="schedule_mail_task_" + str(scheduled_time),
            task="send_mail_app.tasks.send_mail_func",
        )
        
        return HttpResponse("Your mail will be sent within 1 minutes")



class ScheduleReportMailView(View):
    def get(self, request):
        schedule, created = CrontabSchedule.objects.get_or_create(hour=18, minute=21)
        task = PeriodicTask.objects.create(
            crontab=schedule,
            name="schedule_mail_task" + str(datetime.now()),
            task="send_mail_app.tasks.send_mail_func",
        )

        return redirect("/api/schedule-report-range/")

class ScheduleReportRangeView(View):
    def get(self, request):
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

        expenses_within_range = Expense.objects.filter(date__range=(start_date, end_date)).values()
        expenses_list = list(expenses_within_range)

        json_response = json.dumps(expenses_list, cls=CompositeEncoder)

        # Call the Celery task asynchronously
        send_report_func.delay(json_response)

        return HttpResponse("Sent Report ranges...")






#  Frontend


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
