from django.db.models import Sum
from django.shortcuts import render
from rest_framework import generics
from django.views.generic import TemplateView

from api.models import Expense
from api.serializers import ExpenseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


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
