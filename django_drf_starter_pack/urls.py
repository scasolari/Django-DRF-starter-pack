from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django_drf_starter_pack import views as api
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r'profile', api.ProfileViewSet)
router.register(r'campaigns', api.CampaignsViewSet)
router.register(r'integrations', api.IntegrationsViewSet)
router.register(r'audiences', api.MailchimpListViewSet)
router.register(r'templates', api.MailchimpTemplateViewSet)
router.register(r'update', api.MailchimpCampaignGetUpdateViewSet)
router.register(r'send', api.MailchimpSendViewSet)
router.register(r'duplicate', api.MailchimpCampaignDuplicateViewSet)
router.register(r'mc-campaigns', api.MailchimpCampaignListViewSet)
router.register(r'mailchimp-import', api.MailchimpCampaignImportViewSet)
router.register(r'audiences', api.AudienceViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]