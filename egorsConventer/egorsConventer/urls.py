"""
URL configuration for egorsConventer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from mainpage.views import index
from mainpage.views import log
from mainpage.views import reg
from egorsConventer import settings
from mainpage.views  import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', index),
    path('mainpage/', index, name="home"),
    path('info/', inf, name="inf"),
    path('gallery/<str:image_name>/', gal, name="gal"),
    path('loginpage/', LoginUser.as_view(), name="log"),
    path('registerpage/', RegisterUser.as_view(), name="reg"),
    path('logout/', logout_user, name="logout"),
]

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
