# Generated by Django 3.1.3 on 2021-06-17 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_campaign_integration'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='from_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='From Name'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='reply_to',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Replay To'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='subject',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Subject Line'),
        ),
    ]