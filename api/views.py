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


def test(request):
    test_func.delay()
    return HttpResponse("Hi, Done")


def send_mail_to_all(request):
    send_mail_func.delay()

    return HttpResponse("Sent Mail")


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
