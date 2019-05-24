"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from images.views import HomePageView, SiteViewSet, ImageViewSet, ImagesAPIRootView, MostRecentImageViewSet

# Routers for REST API
class ImagesRouter(routers.DefaultRouter):
    APIRootView = ImagesAPIRootView


router = ImagesRouter()
router.register(r'sites', SiteViewSet)
router.register(r'images', ImageViewSet)
router.register(r'images_mostrecent', MostRecentImageViewSet, base_name='Images')

urlpatterns = [
    url(r'^$', HomePageView.as_view()),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
