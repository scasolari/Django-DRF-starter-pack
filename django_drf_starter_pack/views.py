from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from audiences.models import Audience
from campaigns.models import Campaign
from integrations.models import Integration
from serializers import ProfileSerializer, CampaignsSerializer, IntegrationsSerializer
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


class ProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_paginated_response(self, data):
        return Response(data[0])

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class CampaignsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()
    serializer_class = CampaignsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_date']

    def get_queryset(self):
        return Campaign.objects.all()

    def create(self, request, *args, **kwargs):
        try:

            title = request.data.get('title')
            integration = request.data.get('integration')

            mc_integration_key = Integration.objects.filter(id=integration).values_list(
                'key', flat=True)
            mc_integration_server = Integration.objects.filter(id=integration).values_list(
                'server', flat=True)

            print(mc_integration_server[0]),
            print(mc_integration_key[0])

            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0]
            })
            response = client.campaigns.create({
                "type": "regular",
                "settings": {
                    "title": title
                }
            })
            data = response
            mailchimp_id = data.get("id")
            mailchimp_web_id = data.get("web_id")
            mailchimp_status = data.get("status")

            Campaign.objects.create(
                author=self.request.user,
                title=title,
                integration_id=integration,
                mailchimp_id=mailchimp_id,
                mailchimp_web_id=mailchimp_web_id,
                mailchimp_status=mailchimp_status,
            )

            return Response({
                'title': title,
                'integration': integration
            })
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            error_message = ("{}".format(error.text))
            return HttpResponse(error_message, 'application/json', status=500)

    def update(self, request, *args, **kwargs):
        try:
            integration = request.data.get('integration')
            mc_integration_key = Integration.objects.filter(id=integration).values_list('key', flat=True)
            mc_integration_server = Integration.objects.filter(id=integration).values_list('server', flat=True)

            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })
            client.campaigns.update(
                request.data.get('mc_campaign'), {
                    "settings": {
                        "title": request.data.get('title'),
                        "subject_line": request.data.get('subject'),
                        "from_name": request.data.get("from_name"),
                        "reply_to": request.data.get("reply_to"),
                        "template_id": int(request.data.get('mailchimp_template'))
                    },
                    "recipients": {
                        "list_id": request.data.get('mailchimp_list'),
                    }
                }
            )

            campaign_title = request.data.get('title')
            current_campaign = request.data.get('campaign')
            mailchimp_template = request.data.get('mailchimp_template')
            mailchimp_list = request.data.get('mailchimp_list')
            subject_line = request.data.get('subject')
            from_name = request.data.get("from_name")
            reply_to = request.data.get("reply_to")

            Campaign.objects.filter(id=current_campaign).update(
                title=campaign_title,
                mailchimp_template=mailchimp_template,
                mailchimp_list=mailchimp_list,
                subject=subject_line,
                from_name=from_name,
                reply_to=reply_to,
            )
            return Response({
                'mc_campaign_name': campaign_title,
                'mailchimp_template': mailchimp_template,
                'mailchimp_list': mailchimp_list,
                'subject_line': subject_line,
                'from_name': from_name,
                'reply_to': reply_to,
            })

        except ApiClientError as error:
            error_message = ("{}".format(error.text))
            return HttpResponse(error_message, 'application/json', status=500)


class MailchimpListViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()

    def list(self, request, *args, **kwargs):
        try:

            mc_integration_key = Integration.objects.filter(id=request.GET.get('int')).values_list('key', flat=True)
            mc_integration_server = Integration.objects.filter(id=request.GET.get('int')).values_list('server',
                                                                                                      flat=True)

            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })

            response = client.lists.get_all_lists(count=999)
            return Response(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return Response("Error: {}".format(error.text))


class IntegrationsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Integration.objects.all()
    serializer_class = IntegrationsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_date']

    def get_queryset(self):
        return Integration.objects.all()


class MailchimpTemplateViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()

    def list(self, request, *args, **kwargs):
        mc_integration_key = Integration.objects.filter(id=request.GET.get('int')).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=request.GET.get('int')).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })

            response = client.templates.list(count=999)
            return Response(response)
        except ApiClientError as error:
            error_message = ("{}".format(error.text))
            return HttpResponse(error_message, 'application/json', status=500)


class MailchimpCampaignGetUpdateViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()
    serializer_class = CampaignsSerializer

    def update(self, request, *args, **kwargs):
        integration = request.data.get('integration')
        mc_integration_key = Integration.objects.filter(id=integration).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=integration).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })
            mc_campaign = request.data.get('mc_campaign')
            response = client.campaigns.get(mc_campaign)

            title = response.get('settings', dict()).get('title')
            status = response.get('status')
            list_id = response.get('recipients', dict()).get('list_id')
            template_id = response.get('settings', dict()).get('template_id')
            subject_line = response.get('settings', dict()).get('subject_line')
            reply_to = response.get('settings', dict()).get('reply_to')
            from_name = response.get('settings', dict()).get('from_name')

            Campaign.objects.filter(id=request.data.get('campaign_id')).update(
                title=title,
                mailchimp_status=status,
                mailchimp_template=template_id,
                mailchimp_list=list_id,
                subject=subject_line,
                from_name=from_name,
                reply_to=reply_to,
            )
            return Response({
                'title': title,
                'template_id': template_id,
                'subject_line': subject_line,
                'reply_to': reply_to,
                'from_name': from_name
            })

        except ApiClientError as error:
            error_message = ("{}".format(error.text))
            return HttpResponse(error_message, 'application/json', status=500)


class MailchimpSendViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()

    def update(self, request, *args, **kwargs):
        integration = request.data.get('integration')
        mc_integration_key = Integration.objects.filter(id=integration).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=integration).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })

            mc_campaign = request.data.get('mc_campaign')
            response = client.campaigns.send(mc_campaign)
            current_campaign = request.data.get('campaign')

            Campaign.objects.filter(id=current_campaign).update(
                mailchimp_status='sent'
            )
            print(response)

            return Response({
                'mailchimp_status': 'sent'
            })
        except ApiClientError as error:
            error_message = ("{}".format(error.text))
            return HttpResponse(error_message, 'application/json', status=500)


class MailchimpCampaignDuplicateViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()
    serializer_class = CampaignsSerializer

    def create(self, request, *args, **kwargs):
        integration = request.data.get('integration')
        mc_integration_key = Integration.objects.filter(id=integration).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=integration).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })
            mc_campaign_id = request.data.get('mc_campaign')
            response = client.campaigns.replicate(mc_campaign_id)

            mailchimp_id = response.get("id")
            mailchimp_web_id = response.get("web_id")
            mailchimp_status = response.get("status")
            campaign_title = response.get('settings', dict()).get('title')
            mailchimp_template = response.get('settings', dict()).get('template_id')
            mailchimp_list = response.get('recipients', dict()).get('list_id')
            subject_line = response.get('settings', dict()).get('subject_line')
            from_name = response.get('settings', dict()).get('from_name')
            reply_to = response.get('settings', dict()).get('reply_to')
            integration = request.data.get("integration")

            print(mailchimp_id)

            Campaign.objects.create(
                author=self.request.user,
                mailchimp_id=mailchimp_id,
                mailchimp_web_id=mailchimp_web_id,
                mailchimp_status=mailchimp_status,
                integration_id=integration,
                title=campaign_title,
                mailchimp_template=mailchimp_template,
                mailchimp_list=mailchimp_list,
                subject=subject_line,
                from_name=from_name,
                reply_to=reply_to,
            )
            return Response({
                'title': campaign_title,
                'mailchimp_id': mailchimp_id,
                'template_id': mailchimp_template,
                'subject_line': subject_line,
                'reply_to': reply_to,
                'from_name': from_name
            })
        except ApiClientError as error:
            error_message = ("{}".format(error.text))
            return HttpResponse(error_message, 'application/json', status=500)


class MailchimpCampaignListViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()

    def list(self, request, *args, **kwargs):
        mc_integration_key = Integration.objects.filter(id=request.GET.get('int')).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=request.GET.get('int')).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })

            response = client.campaigns.list(count=999)
            return Response(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return Response("Error: {}".format(error.text))

    def retrieve(self, request, pk=None, *args, **kwargs):
        mc_integration_key = Integration.objects.filter(id=request.GET.get('int')).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=request.GET.get('int')).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })

            response = client.campaigns.get(pk)
            return Response(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return Response("Error: {}".format(error.text))


class MailchimpCampaignImportViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Campaign.objects.all()

    def create(self, request, *args, **kwargs):
        integration = request.data.get('integration_id')
        mailchimp_id = request.data.get('id')
        mailchimp_web_id = request.data.get('web_id')
        mailchimp_status = request.data.get('status')
        mailchimp_list = request.data.get('list_id')
        mailchimp_template = request.data.get('template_id')
        subject_line = request.data.get('subject_line')
        from_name = request.data.get('from_name')
        reply_to = request.data.get('reply_to')
        mc_campaign_name = request.data.get('title')

        if Campaign.objects.filter(mailchimp_id=mailchimp_id).exists():
            error_message = ['Campaign already exists']
            return HttpResponse(error_message, 'application/json', status=500)
        else:
            Campaign.objects.create(
                author=self.request.user,
                integration_id=integration,
                mailchimp_id=mailchimp_id,
                mailchimp_web_id=mailchimp_web_id,
                mailchimp_status=mailchimp_status,
                mailchimp_list=mailchimp_list,
                mailchimp_template=mailchimp_template,
                subject=subject_line,
                from_name=from_name,
                reply_to=reply_to,
                title=mc_campaign_name,
            )
            return Response({
                'integration': integration,
                'mailchimp_id': mailchimp_id,
                'mailchimp_web_id': mailchimp_web_id,
                'mailchimp_status': mailchimp_status,
                'mailchimp_list': mailchimp_list,
                'mailchimp_template': mailchimp_template,
                'subject_line': subject_line,
                'from_name': from_name,
                'reply_to': reply_to,
                'mc_campaign_name': mc_campaign_name
            })


class AudienceViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Audience.objects.all()

    def list(self, request, *args, **kwargs):
        mc_integration_key = Integration.objects.filter(id=request.GET.get('int')).values_list('key', flat=True)
        mc_integration_server = Integration.objects.filter(id=request.GET.get('int')).values_list('server', flat=True)

        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mc_integration_key[0],
                "server": mc_integration_server[0],
            })

            response = client.lists.get_all_lists()
            print(response)
            return Response(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
