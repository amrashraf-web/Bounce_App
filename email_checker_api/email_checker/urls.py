from django.urls import path
from email_checker.views import check_emails

urlpatterns = [
    path("check-emails/", check_emails, name="check_emails"),
]
