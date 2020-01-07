from django.urls import path
from . import apis

urlpatterns_api_tables = [
    # path('user_list/', apis.RecipeEditorAPIView.as_view()),
    path('table-list/', apis.TableListAPI.as_view()),
    path('monthly-tables/', apis.MonthlyTableListAPI.as_view()),
    path('main-page/', apis.MainPageAPI.as_view()),
    path('make-log/', apis.MakeTableLogAPI.as_view()),
    path('search/', apis.TableSearchAPI.as_view()),
    # path('recipe/<int:pk>/', apis.RecipeEditorAPIView.as_view())
]

