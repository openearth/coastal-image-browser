from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from serializers import SiteSerializer, ImageSerializer
from models import Images, Sites

from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

# ViewSets define the view behavior.


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()#filter(inarchive=1)
    serializer_class = ImageSerializer
    http_method_names = ['get',]
    pagination_class = LargeResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('site', 'camera', 'dayminute', 'epoch')
    ordering_fields = ('site', 'camera', 'epoch')


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Sites.objects.filter(openaccess=1)
    serializer_class = SiteSerializer
    http_method_names = ['get',]