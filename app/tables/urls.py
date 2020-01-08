from django.urls import path
from . import apis

urlpatterns_api_tables = [
    path('table-list/', apis.TableListAPI.as_view()),
    path('monthly-tables/', apis.MonthlyTableListAPI.as_view()),
    path('main-page/', apis.MainPageAPI.as_view()),
    path('make-log/', apis.MakeTableLogAPI.as_view()),
    path('search/', apis.TableSearchAPI.as_view()),
]

