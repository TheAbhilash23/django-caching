from rest_framework import routers

from profiles import views

router = routers.DefaultRouter()
router.register(r'Profile', views.ProfileViewSet, basename='profile_api')
