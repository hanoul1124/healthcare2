from django.urls import path
from . import apis

urlpatterns_api_tables = [
    path('user_list/', apis.ExampleAPIView.as_view())
]

