from django.contrib import admin
from django.urls import path, include

from .views import (
    ExpenseCreateView,
    ExpenseHistoryView,
    ExpenseHistoryIdView,
    TotalExpenseWithDateView,
    ExpenseHistoryWithDateView,
    get_csrf_token,
)

from . import views

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
    #
    path("get-csrf-token/", get_csrf_token, name="get-csrf-token"),
    path("", views.test, name="test"),
    path("sendmail/", views.send_mail_to_all, name="sendmail"),
    path("send-report/", views.send_report, name="send-report-func"),
    path("send-report-range/", views.send_report_range, name="send-report-func"),
    path("schedule-mail/", views.schedule_mail, name="schedule-mail"),
    path(
        "schedule-report-mail/", views.schedule_report_mail, name="schedule-report-mail"
    ),
    path(
        "schedule-report-range/",
        views.schedule_report_range,
        name="schedule-report-range",
    ),
]
