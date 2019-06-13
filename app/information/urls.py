from rest_framework.routers import SimpleRouter

from . import views

fni_router = SimpleRouter()
fni_router.register(
    prefix='fni',
    base_name='FNI',
    viewset=views.FNIViewSet
)

urlpatterns_fni_information = fni_router.urls

hfi_router = SimpleRouter()
hfi_router.register(
    prefix='hfi',
    base_name='HFI',
    viewset=views.HFIViewSet
)

urlpatterns_hfi_information = hfi_router.urls


# I-0050 : 건강기능식품 개별인정형 정보
# I-0040 : 건강기능식품 기능성 원료 인정현황
# I2710 : 건강기능식품 품목 분류정보