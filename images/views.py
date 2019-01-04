from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, routers
from .serializers import SiteSerializer, ImageSerializer
from .models import Images, Sites

from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework


class ImagesAPIRootView(routers.APIRootView):
    """
    Coastal Images API
    """


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# ViewSets define the view behavior.


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows images to be viewed

    list:
    List all images
    """
    queryset = Images.objects.filter(inarchive=1)
    serializer_class = ImageSerializer
    http_method_names = ['get',]
    pagination_class = LargeResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('site', 'camera', 'dayminute', 'epoch')
    ordering_fields = ('site', 'camera', 'epoch')


class SiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sites to be viewed

    retrieve:
    Show site instance

    list:
    List all sites
    """
    queryset = Sites.objects.filter(openaccess=1)
    serializer_class = SiteSerializer
    http_method_names = ['get',]
