from django.shortcuts import render
from django.db.models import Min, Max
from django.views.generic import TemplateView

import pandas
import datetime

from images.models import Images, Sites
from highcharts.views import HighChartsHeatMapView


# Create your views here.

class IndexView(TemplateView):
    site = 'all'
    height = 400
    template_name = 'dashboard/heatmap.html'

    def get(self, request, *args, **kwargs):
        if kwargs['site'] is not None:
            query = Sites.objects.filter(site=kwargs['site'])
            if query.count() == 1:
                self.site = kwargs['site']
                HM = HeatMap()
                HM.site = self.site
                self.height = HM.cameras[-1] * 70

        return super(IndexView, self).get(request)


class HeatMap(HighChartsHeatMapView):
    site = None
    epoch = datetime.datetime.utcfromtimestamp(0)
    tooltip = {'headerFormat': 'Images: ',
               'pointFormat': '{point.value}<br/>'}

    def get_ajax(self, request, *args, **kwargs):
        query = Sites.objects.filter(site=kwargs['site'])
        if query.count() == 1:
            self.site = kwargs['site']
        else:
            self.site = None
        return super(HeatMap, self).get_ajax(request)

    @property
    def title(self):
        if self.site is None:
            return 'Acquired images'
        else:
            return 'Acquired images at %s' % self.site

    @property
    def subtitle(self):
        if self.site is None:
            return 'counts per site per day'
        else:
            return 'counts per camera per day'

    @property
    def sites(self):
        sites = []
        epoch__gte = (self.get_dates()[0] - self.epoch).total_seconds()
        for site in Sites.objects.filter(openaccess=1).values_list('site', flat=True):
            if Images.objects.filter(site=site, epoch__gte=epoch__gte):
                sites.append(site)
        return sites

    @property
    def cameras(self):
        epoch__gte = (self.get_dates()[0] - self.epoch).total_seconds()
        query = Images.objects.filter(site=self.site, epoch__gte=epoch__gte)
        aggregate = query.aggregate(Max('camera'))
        return list(range(1, aggregate['camera__max']+1))

    @property
    def yaxis(self):
        if self.site is None:
            y_axis = {'categories': self.sites, 'title': None}
        else:
            y_axis = {'categories': self.cameras, 'title': None}
        return y_axis

    def get_dates(self):
        return pandas.date_range(end=datetime.datetime.utcnow(),
                                 periods=14,
                                 normalize=True)

    @property
    def categories(self):
        return [d.strftime('%a %d %b %Y') for d in self.get_dates()]

    @property
    def coloraxis(self):
        return {
            'min': 0,
            'minColor': '#FFFFFF',
            'maxColor': '#7cb5ec'
        }

    @property
    def series(self):

        epoch__gte = [(d-self.epoch).total_seconds() for d in self.get_dates()]
        epoch__lt = [daystart+86400 for daystart in epoch__gte]
        if self.site is None:
            query0 = Images.objects.filter(epoch__gte=epoch__gte[0], epoch__lt=epoch__lt[-1])
        else:
            query0 = Images.objects.filter(epoch__gte=epoch__gte[0], epoch__lt=epoch__lt[-1], site=self.site)
        data = []

        for i, (gte, lt) in enumerate(zip(epoch__gte, epoch__lt)):
            daydata = query0.filter(epoch__gte=gte, epoch__lt=lt)
            if self.site is None:
                for j, site in enumerate(self.sites):
                    sitedaydata = daydata.filter(site=site)
                    data.append([i, j, sitedaydata.count()])
            else:
                for j, camera in enumerate(self.cameras):
                    cameradaydata = daydata.filter(camera=camera)
                    data.append([i, j, cameradaydata.count()])

        series = [
            {
                'data': data,
                'borderWidth': 1,
                'dataLabels': {'enabled': True, 'color': '#000000'}
            },
        ]
        return series
