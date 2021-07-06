from django.contrib.auth.models import User
from rest_framework import serializers
from campaigns.models import Campaign
from integrations.models import Integration


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'is_staff']


class CampaignsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Or User.objects.filter(active=True)
        required=False,
        allow_null=True,
        default=None
    )
    title = serializers.CharField(required=True)

    def validate_author(self, value):
        return self.context['request'].user

    class Meta:
        model = Campaign
        fields = ['id', 'author', 'title', 'mailchimp_id', 'mailchimp_web_id', 'mailchimp_status', 'integration', 'subject', 'from_name', 'reply_to', 'mailchimp_list', 'mailchimp_template', 'created_date', ]


class IntegrationsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Or User.objects.filter(active=True)
        required=False,
        allow_null=True,
        default=None
    )

    def validate_author(self, value):
        return self.context['request'].user

    class Meta:
        model = Integration
        fields = ['id', 'author', 'title', 'key', 'server', 'created_date', ]
