from rest_framework import serializers
from image_api.models import Image


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    thumbnails = serializers.SerializerMethodField('get_thumbnails')
    original_image = serializers.SerializerMethodField('get_original_image')
    expiring_link = serializers.SerializerMethodField('get_expiring_link')

    class Meta:
        model = Image
        fields = ['url', 'id', 'thumbnails', 'original_image', 'expiring_link']

    def get_thumbnails(self, obj):
        data = list(self.context['request'].user.plan.height.values_list())
        heights = []
        for item in data:
            if self.context['request'].build_absolute_uri().endswith(self.context['request'].get_host() + '/'):
                heights.append(self.context['request'].build_absolute_uri(str(obj.id) + '/thumbnail/' + str(item[1])))
            else:
                heights.append(self.context['request'].build_absolute_uri('thumbnail/' + str(item[1])))
        return heights

    def get_original_image(self, obj):
        if self.context['request'].user.plan.original_image:
            if self.context['request'].build_absolute_uri().endswith(self.context['request'].get_host() + '/'):
                return self.context['request'].build_absolute_uri(str(obj.id) + '/original/')
            else:
                return self.context['request'].build_absolute_uri('original/')
        else:
            return False

    def get_expiring_link(self, obj):
        if self.context['request'].user.plan.expiring_link:
            if self.context['request'].build_absolute_uri().endswith(self.context['request'].get_host() + '/'):
                return self.context['request'].build_absolute_uri(str(obj.id) + '/' + obj.expiring_link)
            else:
                return self.context['request'].build_absolute_uri(obj.expiring_link)
        else:
            return False


class ImageSerializerCreateUpdate(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ['url', 'id', 'image']


class ImageSerializerCreateUpdateTime(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ['url', 'id', 'image', 'time']


class ImageSerializerExpiring(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ['url', 'id']
