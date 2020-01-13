"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from members.urls import urlpatterns_api_members
from tables.urls import urlpatterns_api_tables
from information.urls import urlpatterns_api_information
from . import views

urlpatterns_api = ([
    path('members/', include(urlpatterns_api_members)),
    path('tables/', include(urlpatterns_api_tables)),
    path('information/', include(urlpatterns_api_information)),
], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/', include(urlpatterns_api)),
]

admin.site.site_header = "App Name 관리자 포털"
admin.site.site_title = "App Name Admin Portal"
admin.site.index_title = "App Name Admin Portal"

urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)