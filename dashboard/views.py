from django.shortcuts import render

import pandas
import datetime

from images.models import Images, Sites
from highcharts.views import HighChartsHeatMapView


# Create your views here.

class HeatMap(HighChartsHeatMapView):
    epoch = datetime.datetime.utcfromtimestamp(0)
    title = 'Acquired images counts per site per day'
    tooltip = {'headerFormat': 'Images: ',
               'pointFormat': '{point.value}<br/>'}

    @property
    def sites(self):
        sites = []
        epoch__gte = (self.get_dates()[0] - self.epoch).total_seconds()
        for site in Sites.objects.filter(openaccess=1).values_list('site', flat=True):
            if Images.objects.filter(site=site, epoch__gte=epoch__gte):
                sites.append(site)
        return sites

    @property
    def yaxis(self):
        y_axis = {'categories': self.sites, 'title': None}
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
        query0 = Images.objects.filter(epoch__gte=epoch__gte[0], epoch__lt=epoch__lt[-1])
        sites = self.sites
        data = []

        for i, (gte, lt) in enumerate(zip(epoch__gte, epoch__lt)):
            daydata = query0.filter(epoch__gte=gte, epoch__lt=lt)
            for j, site in enumerate(sites):
                sitedaydata = daydata.filter(site=site)
                data.append([i, j, sitedaydata.count()])

        series = [
            {
                'data': data,
                'borderWidth': 1,
                'dataLabels': {'enabled': True, 'color': '#000000'}
            },
        ]
        return series