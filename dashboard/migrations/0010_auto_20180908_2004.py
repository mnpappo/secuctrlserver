# Generated by Django 2.1.1 on 2018-09-08 20:04

from django.db import migrations
import django_geoposition_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20180908_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='position',
            field=django_geoposition_field.fields.GeopositionField(max_length=100),
        ),
    ]
