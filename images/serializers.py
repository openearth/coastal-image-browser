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
    url = serializers.SerializerMethodField()

    def get_url(self, images):
        request = self.context.get('request')
        url = '/sites%s' % images.location
        return request.build_absolute_uri(url)

    class Meta:
        model = Images
        fields = (
            'url',
            'site',
            'epoch',
            'camera',
            'image_type',
            'day_minute',
        )
