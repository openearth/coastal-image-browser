from rest_framework import serializers
from images.models import Sites, Images


# Serializers define the API representation.

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sites
        fields = (
            'site',
            'country',
            'description',
            'mincam',
            'maxcam',
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = (
            'url',
            'site',
            'epoch',
            'camera',
            'type',
            'dayminute',
        )