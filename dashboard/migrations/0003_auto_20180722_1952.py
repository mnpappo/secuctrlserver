# Generated by Django 2.0.7 on 2018-07-22 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20180722_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='protocol',
            field=models.CharField(blank=True, choices=[('http', 'HTTP'), ('https', 'HTTPS')], default='http', help_text='Select Device Connection Protocol', max_length=1),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_ip',
            field=models.GenericIPAddressField(help_text='Set Device IP Address, E.G. 192.168.1.103'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_port',
            field=models.PositiveIntegerField(help_text='Set Device Port, E.G. 5000', null=True, verbose_name='Device Port Address'),
        ),
    ]
