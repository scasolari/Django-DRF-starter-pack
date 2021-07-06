# Generated by Django 3.1.3 on 2021-06-16 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0003_auto_20210616_0947'),
        ('campaigns', '0004_auto_20210616_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='integration',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='integrations.integration', verbose_name='Integration'),
        ),
    ]