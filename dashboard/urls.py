from django.conf.urls import url
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='dashboard/heatmap.html'), name='heatmap'),
    url(regex='^json/heatmap$', view=views.HeatMap.as_view(), name='json-heatmap'),
]
