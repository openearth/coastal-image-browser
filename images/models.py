from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Sites(models.Model):
    site = models.CharField(primary_key=True, max_length=16)
    country = models.CharField(max_length=2, blank=True, null=True)
    utcoffset = models.IntegerField(db_column='utcOffset', blank=True, null=True)  # Field name made lowercase.
    mincam = models.IntegerField(db_column='minCam', blank=True, null=True)  # Field name made lowercase.
    maxcam = models.IntegerField(db_column='maxCam', blank=True, null=True)  # Field name made lowercase.
    accessgroup = models.IntegerField(db_column='accessGroup', blank=True, null=True)  # Field name made lowercase.
    openaccess = models.IntegerField(db_column='openAccess', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=128, blank=True, null=True)
    epochstart = models.IntegerField(db_column='epochStart', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sites'
        ordering = ('site',)


class Images(models.Model):
    location = models.CharField(primary_key=True, max_length=128)
    site = models.CharField(max_length=16)
    epoch = models.IntegerField()
    camera = models.IntegerField()
    type = models.CharField(max_length=16)
    dayminute = models.SmallIntegerField(blank=True, null=True)
    inarchive = models.IntegerField(blank=True, null=True)

    @property
    def url(self):
        return 'http://argus-public.deltares.nl/sites%s' % self.location

    class Meta:
        managed = False
        db_table = 'Images'
        ordering = ('-epoch', 'camera')
