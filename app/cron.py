from django.core.cache import cache

from .tables.models import TableLog


def table_renewal_job():
    cache.delete('table_list')
    cache.delete('today_table')


def table_log_renewal_job():
    TableLog.objects.all().delete()