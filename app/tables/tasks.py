import calendar
import datetime
from .models import *
from members.models import User
from config.celery import app


# for celery test
@app.task
def table_renewal():
    cache.delete('table_list')
    cache.delete('today_table')


@app.task
def table_log_renewal():
    TableLog.objects.all().delete()


@app.task
def make_default_log_daily(user_pk):
    date_range = [
        datetime.date.today().replace(day=1) + datetime.timedelta(i)
        for i in range(0, calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])
    ]
    for date in date_range:
        for time in ['Breakfast', 'Lunch', 'Dinner', 'Snack']:
            TableLog.objects.get_or_create(user=User.objects.get(pk=user_pk), date=date, time=time)


@app.task
def make_default_log_monthly():
    user_list = User.objects.values_list('pk', flat=True)
    for user_pk in user_list:
        make_default_log_daily.delay(user_pk)
