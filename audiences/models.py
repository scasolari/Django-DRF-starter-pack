from django.contrib.auth.models import User
from django.db import models


class Audience(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Author')
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name='Audience Title')

    def __str__(self):
        return self.title
