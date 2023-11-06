from django.urls import path, include
#from pass_app import views
from .views import MountViewSet, CoordsViewSet, PhotoViewSet, LevelViewSet, MountDetailViewSet, EmailAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pass', MountViewSet, basename='pass')
router.register(r'coords', CoordsViewSet, basename='coords')
router.register(r'photo', PhotoViewSet, basename='photo')
router.register(r'level', LevelViewSet, basename='levels')


urlpatterns = [
    # Sprint 1
    path('submitData/', include(router.urls)),
    # Sprint 2
    path('submitData/<int:pk>/', MountDetailViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('submitData/user__email=<str:email>', EmailAPIView.as_view()),
]