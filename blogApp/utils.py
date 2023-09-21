from django.core.mail import send_mail
from django.conf import settings
import asyncio
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.shortcuts import render, redirect


async def send_new_blog_notification(title):
    subject = f'New Blog Added - {title}'
    from_email = settings.DEFAULT_FROM_EMAIL

    admin_users = User.objects.filter(is_staff=True)

    for admin_user in admin_users:
        recipient_email = admin_user.email
        recipient_first_name = admin_user.username

        message = f'Hi {recipient_first_name},\n\nA new blog has been added with the title: {title}.\n\nBest regards,\nXOVOLT Team'

        recipient_list = [recipient_email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Handle the exception, possibly log it
            print(f"Failed to send email to {recipient_email}: {e}")