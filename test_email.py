import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Trip_Registration.settings')
django.setup()

from django.core.mail import send_mail

send_mail(
    'בדיקה',
    'זהו מייל בדיקה מ-Django',
    'yair6655@gmail.com',
    ['yair6655@gmail.com'],
    fail_silently=False,
)
