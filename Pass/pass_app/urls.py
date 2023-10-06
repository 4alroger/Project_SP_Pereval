from django.urls import path, include
#from pass_app import views
from .views import MountViewSet, CoordsViewSet, PhotoViewSet, LevelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pass', MountViewSet, basename='pass')
router.register(r'coords', CoordsViewSet, basename='coords')
router.register(r'photo', PhotoViewSet, basename='photo')
router.register(r'level', LevelViewSet, basename='levels')


urlpatterns = [
    path('submitData/', include(router.urls)),
]