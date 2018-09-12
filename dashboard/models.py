from django.db import models
from geoposition.fields import GeopositionField
from django.utils.timezone import now
# from django_geoposition_field.fields import GeopositionField


# Create your models here.

class Client(models.Model):
    client_name = models.CharField(max_length=40, help_text="Enetr Client Name Here, Max 40 Chars", verbose_name='Client Name')
    client_email = models.EmailField(max_length=40, help_text="Enter Client Email Here", verbose_name='Client Email')
    client_phone = models.CharField(max_length=15, help_text="Enter Client Phone Number Here, Do not include +88", verbose_name='Client Phone')
    
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.client_name


class Device(models.Model):
    PROTOCOLS = (
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
    )

    STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    device_code_name = models.CharField(max_length=40, help_text="Enter The Device Codename, Max 40 Chars(E.G. DBBL-1209-01)", verbose_name='Device Codename')
    device_status = models.CharField(max_length=10, choices=STATUS, help_text="Do You Want To Accept Data From This Device?", verbose_name='Device Status', default='inactive')
    position_address = models.CharField(max_length=100, help_text="Enter The Device Location Address, Max 100 Chars(E.G. 322, Concept Tower, Panthopath, Dhaka - 1209)", verbose_name='Device Position Address')
    position = GeopositionField(help_text="Enter Lattitude and Longitude Here, Please Select from Map")
    protocol = models.CharField(max_length=5, choices=PROTOCOLS, blank=True, default='http', help_text='Select Device Connection Protocol')
    device_ip = models.GenericIPAddressField(help_text="Set Device IP Address, E.G. 192.168.1.103")
    device_port = models.PositiveIntegerField(help_text="Set Device Port, E.G. 5000", verbose_name='Device Port Address', null=True)
    lattitude = models.DecimalField(decimal_places=10, max_digits=100, help_text="Posision", null=True, default=123.123)
    longitude = models.DecimalField(decimal_places=10, max_digits=100, help_text="Posision", null=True, default=123.123)
    client_name = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.device_code_name



class Settings(models.Model):
    pass


class GuardAttendance(models.Model):
    pass


class Guard(models.Model):
    name = models.CharField(max_length=40, help_text="Guard's Name")
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)
    device = models.ForeignKey('Device', on_delete=models.SET_NULL, null=True)
    schedule_time_from = models.TimeField(name="Schedule Time - From")
    schedule_time_to = models.TimeField(name="Schedule Time - To")

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.name


class NotificationLog(models.Model):
    STATUS = (
        ('monitor', 'Monitor'),
        ('false', 'False Alarm'),
        ('warning', 'Warning'),
        ('intrusion', 'Intrusion'),
    )
    sensor_name = models.CharField(max_length=100, help_text="From Which Sensor the Inrusion Occured")
    sensor_value = models.CharField(max_length=100, help_text="From Which Sensor the Inrusion Occured", default='None')
    notification_status = models.CharField(choices=STATUS, max_length=10, help_text="Notification Type", default='monitor')
    device = models.ForeignKey('Device', on_delete=models.SET_NULL, null=True)
    notification_time = models.DateTimeField(help_text="When the inrusion created at device.", default=now, blank=True)

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return self.sensor_name


