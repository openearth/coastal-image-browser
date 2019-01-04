from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, routers
from .serializers import SiteSerializer, ImageSerializer
from .models import Images, Sites

from rest_framework.pagination import PageNumberPagination
from django_filters import FilterSet, ChoiceFilter, rest_framework
from django.db.models import Max


# obtain site choices from site table
SITE_CHOICES = Sites.objects.values_list('site', 'description')
# construct image type choices, using list comprehension and set because distinct is not supported by the database backend
IMAGE_TYPE_CHOICES = [(image_type, image_type) for image_type in set(Images.objects.values_list('image_type', flat=True))]
# construct camera choices, using list comprehension and set because distinct is not supported by the database backend
CAMERA_CHOICES = [(cam_num, cam_num) for cam_num in set(Images.objects.values_list('camera', flat=True))]
# construct camera choices, using list comprehension and set because distinct is not supported by the database backend
DAY_MINUTE_CHOICES = [(day_minute, "{}  ({}:{:02d})".format(day_minute, day_minute//60, day_minute%60)) for day_minute in sorted(set(Images.objects.values_list('day_minute', flat=True)))]


# for documentation purposes: the docstring is used as title in the API root view
class ImagesAPIRootView(routers.APIRootView):
    """
    Coastal Images API
    """


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ImageFilter(FilterSet):
    """
    Image filter class to provide sensible choices
    """
    site = ChoiceFilter(choices=SITE_CHOICES)
    image_type = ChoiceFilter(choices=IMAGE_TYPE_CHOICES)
    camera = ChoiceFilter(choices=CAMERA_CHOICES)
    day_minute = ChoiceFilter(choices=DAY_MINUTE_CHOICES)

    class Meta:
        model = Images
        fields = ('site', 'image_type', 'camera', 'day_minute', 'epoch')


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
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = ImageFilter
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
