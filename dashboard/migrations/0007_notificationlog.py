# Generated by Django 2.1.1 on 2018-09-08 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20180906_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_name', models.CharField(help_text='From Which Sensor the Inrusion Occured', max_length=40)),
                ('When the inrusion created at device.', models.DateTimeField()),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Device')),
            ],
        ),
    ]
