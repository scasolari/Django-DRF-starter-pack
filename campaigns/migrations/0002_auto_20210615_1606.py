# Generated by Django 3.1.3 on 2021-06-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Campaign Name'),
        ),
    ]
