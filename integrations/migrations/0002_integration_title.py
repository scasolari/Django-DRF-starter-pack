# Generated by Django 3.1.3 on 2021-06-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='integration',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='Integration Title'),
        ),
    ]
