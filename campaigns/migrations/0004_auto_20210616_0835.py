# Generated by Django 3.1.3 on 2021-06-16 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_auto_20210616_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='mailchimp_id',
            field=models.CharField(max_length=200, verbose_name='Mailchimp ID'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='mailchimp_status',
            field=models.CharField(max_length=200, verbose_name='Mailchimp Status'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='mailchimp_web_id',
            field=models.CharField(max_length=200, verbose_name='Mailchimp Web ID'),
        ),
    ]
