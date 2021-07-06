from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Integration(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Author')
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name='Integration Title')
    key = models.CharField(max_length=200, blank=False, null=False, verbose_name='Integration Key')
    server = models.CharField(max_length=200, blank=False, null=False, verbose_name='Integration Server')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
