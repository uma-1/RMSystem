from django.urls import path, include
from rest_framework import routers
from .views import BannerApiDetails

router = routers.DefaultRouter()
router.register('', BannerApiDetails)

urlpatterns = [
    path('', include(router.urls))
]
