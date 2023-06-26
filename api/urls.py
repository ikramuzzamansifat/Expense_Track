from django.contrib import admin
from django.urls import path, include

from .views import (
    ExpenseCreateView,
    ExpenseHistoryView,
    ExpenseHistoryIdView,
    TotalExpenseWithDateView,
    ExpenseHistoryWithDateView,
)

urlpatterns = [
    # Frontend


    # Backend
    path("create-expense/", ExpenseCreateView.as_view(), name="expense-create"),
    path("expense-history/", ExpenseHistoryView.as_view(), name="expense-history"),
    path(
        "expense-history/<int:pk>",
        ExpenseHistoryIdView.as_view(),
        name="expense-history-id",
    ),
    path(
        "expense-history/<str:date>",
        ExpenseHistoryWithDateView.as_view(),
        name="expense-history-with-date",
    ),
    path(
        "total-expense/<str:date>",
        TotalExpenseWithDateView.as_view(),
        name="total-expense-with-date",
    ),
]
