from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django_drf_starter_pack import views as profile
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'profile', profile.ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]