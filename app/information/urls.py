# I-0050 : 건강기능식품 개별인정형 정보
# I-0040 : 건강기능식품 기능성 원료 인정현황
# I2710 : 건강기능식품 품목 분류정보
from django.urls import path
from . import apis


urlpatterns_api_information = [
    path('fni/', apis.FNISearchView.as_view()),
    path('hfi/', apis.HFISearchView.as_view()),
    path('hfa/', apis.HFASearchView.as_view()),
    path('hfc/', apis.HFCSearchView.as_view()),
]