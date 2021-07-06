from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from integrations.models import Integration


class Campaign(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Author')
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name='Campaign Name')
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Integration', default='')
    mailchimp_id = models.CharField(max_length=200, blank=False, null=False, verbose_name='Mailchimp ID')
    mailchimp_web_id = models.CharField(max_length=200, blank=False, null=False, verbose_name='Mailchimp Web ID')
    mailchimp_status = models.CharField(max_length=200, blank=False, null=False, verbose_name='Mailchimp Status')
    subject = models.CharField(max_length=200, verbose_name='Subject Line', null=True, blank=True)
    from_name = models.CharField(max_length=200, verbose_name='From Name', null=True, blank=True)
    reply_to = models.CharField(max_length=200, verbose_name='Replay To', null=True, blank=True)
    mailchimp_list = models.CharField(max_length=200, verbose_name='Mailchimp List', null=True, blank=True)
    mailchimp_template = models.CharField(max_length=200, verbose_name='Mailchimp Template', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
