from django.urls import path
from . import apis

urlpatterns_api_tables = [
    path('user_list/', apis.ExampleAPIView.as_view()),
    # path('today-table/', apis.TodayTableAPI.as_view()),
    path('table-list/', apis.TableListAPI.as_view()),
    path('main-page/', apis.MainPageAPI.as_view()),
    path('make-log/', apis.MakeTableLogAPI.as_view()),
    path('search/', apis.TableSearchAPI.as_view())
]

