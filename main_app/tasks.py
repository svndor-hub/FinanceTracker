from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum
from .models import Transaction
from django.contrib.auth.models import User


@shared_task
def send_weekly_summary():
    # Fetch all users
    users = User.objects.all()

    for user in users:
        # Calculate total income and expenses for the past week
        weekly_transactions = Transaction.objects.filter(
            user=user,
            date__week=datetime.now().isocalendar()[1]
        )
        income = weekly_transactions.filter(category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = weekly_transactions.filter(category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        # Send email
        send_mail(
            subject="Your Weekly Financial Summary",
            message=f"""
                Hello {user.username},

                Here is your financial summary for the week:

                Total Income: ${income:.2f}
                Total Expenses: ${expenses:.2f}
            """,
            from_email="no-reply@financetracker.com",
            recipient_list=[user.email],
        )
