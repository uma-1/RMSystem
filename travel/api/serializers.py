from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Banner


class BannerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
