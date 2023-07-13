from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    # Backend
    path("create-expense/", views.ExpenseCreateView.as_view(), name="expense-create"),
    path("expense-history/", views.ExpenseHistoryView.as_view(), name="expense-history"),
    path("expense-history/<int:pk>", views.ExpenseHistoryIdView.as_view(),name="expense-history-id"),
    path("expense-history/<str:date>", views.ExpenseHistoryWithDateView.as_view(),name="expense-history-with-date"),
    path("total-expense/<str:date>", views.TotalExpenseWithDateView.as_view(),name="total-expense-with-date"
    ),
    
    #Utilities 
    path("get-csrf-token/", views.get_csrf_token, name="get-csrf-token"),
    path("", views.TestView.as_view(), name="test"),
    
    # Celery Tasks  
    path("send-mail/", views.SendMailView.as_view(), name="send-mail"),
    path("send-report-range/", views.SendReportRangeView.as_view(), name="send-report-func"),
    # path("send-report-range/", views.send_report_range, name="send-report-func"),
    
    # path("schedule-mail/", views.schedule_mail, name="schedule-mail"),
    path("schedule-mail/", views.ScheduleMailView.as_view(), name="schedule-mail"),
    path("schedule-report-mail/", views.ScheduleReportMailView.as_view(), name="schedule-report-mail"),
    path("schedule-report-range/", views.ScheduleReportRangeView.as_view(), name="schedule-report-range"),
]
