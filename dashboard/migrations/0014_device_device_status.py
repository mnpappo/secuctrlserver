# Generated by Django 2.1.1 on 2018-09-08 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20180908_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='device_status',
            field=models.CharField(default='inactive', help_text='Do You Want To Accept Data From This Device?', max_length=10, verbose_name='Device Status'),
        ),
    ]
