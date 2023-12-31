from rest_framework import serializers
from profiles import models
import base64
from caching import cache_this


class ProfileSerializer(serializers.ModelSerializer):
    Base64Picture = serializers.SerializerMethodField()

    @cache_this
    def get_Base64Picture(self, obj):
        import time
        time.sleep(5)
        data = base64.b64encode(obj.Picture.read())
        return data

    class Meta:
        model = models.Profile
        exclude = ()

