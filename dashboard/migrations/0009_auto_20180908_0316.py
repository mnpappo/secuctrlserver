# Generated by Django 2.1.1 on 2018-09-08 03:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_notificationlog_sensor_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationlog',
            name='When the inrusion created at device.',
        ),
        migrations.AddField(
            model_name='notificationlog',
            name='notification_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='When the inrusion created at device.'),
        ),
    ]
