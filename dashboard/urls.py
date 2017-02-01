from django.conf.urls import url

from views import IndexView, HeatMap


urlpatterns = [
    url(r'^(?P<site>[a-z]+)?$', IndexView.as_view(), name='heatmap-site'),
    url(regex='^json/heatmap/(?P<site>[a-z]+)$', view=HeatMap.as_view(), name='json-heatmap'),
]
