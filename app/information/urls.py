# from rest_framework.routers import SimpleRouter
#
# from . import views
#
# # fni
# fni_router = SimpleRouter()
# fni_router.register(
#     prefix='fni',
#     base_name='FNI',
#     viewset=views.FNIViewSet
# )
#
# urlpatterns_fni_information = fni_router.urls
#
# # hfi
# hfi_router = SimpleRouter()
# hfi_router.register(
#     prefix='hfi',
#     base_name='HFI',
#     viewset=views.HFIViewSet
# )
# urlpatterns_hfi_information = hfi_router.urls
#
#
# # hfc
# hfc_router = SimpleRouter()
# hfc_router.register(
#     prefix='hfc',
#     base_name='HFC',
#     viewset=views.HFCViewSet
# )
#
# urlpatterns_hfc_information = hfc_router.urls
#
#
# # hfa
# hfa_router = SimpleRouter()
# hfa_router.register(
#     prefix='hfa',
#     base_name='HFA',
#     viewset=views.HFAViewSet
# )
#
# urlpatterns_hfa_information = hfa_router.urls

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