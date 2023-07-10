"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import (
    IndexView,
    HistoryView,
    HistoryDateView,
    CreateExpense,
    HistoryReportView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", IndexView.as_view(), name="index"),
    path("history/", HistoryView.as_view(), name="history"),
    path("history_date/", HistoryDateView.as_view(), name="history-date"),
    path("expense_create/", CreateExpense.as_view(), name="expense-create"),
    path("history_report/", HistoryReportView.as_view(), name="history-report"),
]
