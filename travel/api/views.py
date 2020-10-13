from .serializers import BannerDataSerializer
from rest_framework import viewsets
from blog.models import Banner

from rest_framework.permissions import IsAuthenticated




class BannerApiDetails(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Banner.objects.all()
    serializer_class = BannerDataSerializer
