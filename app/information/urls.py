from rest_framework.routers import SimpleRouter

from . import views

app_name = 'FNIs'

router = SimpleRouter()
router.register(
    prefix=r'',
    base_name='FNIs',
    viewset=views.FNIViewSet
)

urlpatterns_api_information = router.urls