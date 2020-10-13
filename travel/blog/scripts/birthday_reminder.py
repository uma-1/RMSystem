from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from ..models import *
from django.conf import settings
from django.utils import timezone
import schedule
import time

today = timezone.now().date()


def run():
    email = settings.EMAIL_HOST_USER
    today = timezone.now().date()
    for reminder in Customer_Records.objects.filter(birthdate__day=today.day, birthdate__month=today.month):
        send_mail("Happy Birthday " + reminder.name,
                  "Wishing you many many happy returns of the day!! Happy Birthday!!! - Teenkanya Travel & Trek.",
                  email,
                  [reminder.email])
        print('Birthday Email Sent to ' + reminder.name)

# schedule.every(10).seconds.do(run)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
