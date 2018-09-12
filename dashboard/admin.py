from django.contrib import admin
from .models import Device, Client, Guard, NotificationLog
import datetime
from django.urls import reverse
from django.utils.html import mark_safe
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# Register your models here.


def status_false_alarm(modeladmin, request, queryset):
    queryset.update(notification_status='false')
status_false_alarm.short_description = "Change To False Alarm"

def status_warning(modeladmin, request, queryset):
    queryset.update(notification_status='warning')
status_warning.short_description = "Change To Warning"

def status_intrusion(modeladmin, request, queryset):
    queryset.update(notification_status='intrusion')
status_intrusion.short_description = "Change To Intrusion"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_email', 'client_phone']

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['sensor_name', 'sensor_value',
                    'device', 'notification_time', 'notification_status']
    
    list_filter = (('notification_time', DateTimeRangeFilter),
                   'sensor_name', 'device', 'notification_status')
    actions = [status_false_alarm, status_warning, status_intrusion]

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_code_name', 'client_name', 'device_ip_port',
                    'position_address', 'position_map', 'device_status', 'action_button']
    
    def device_ip_port(self, obj):
        return '{protocol}://{ip}:{port}'.format(protocol = obj.protocol, ip = obj.device_ip, port = obj.device_port)
    device_ip_port.short_description = 'Device IP Port Address'
    device_ip_port.allow_tags = True
    
    def action_button(self, obj):
        return mark_safe('<a target="_blank" class="button" href="{protocol}://{ip}:{port}"> Monitor This Device Now </a>'.format(protocol=obj.protocol, ip=obj.device_ip, port=obj.device_port))
    action_button.allow_tags = True
    action_button.short_description = 'Device Action'
        
    def position_map(self, instance):
        if instance.position is not None:
            return mark_safe('<img src="http://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size={width}x{height}&maptype=roadmap&markers={latitude},{longitude}&sensor=false&visual_refresh=true&scale={scale}" width="{width}" height="{height}">'.format(
                latitude = instance.position.latitude,
                longitude = instance.position.longitude,
                zoom = 15,
                width = 200,
                height = 100,
                scale = 2
            ))
    position_map.allow_tags = True

    list_filter = ('client_name',)


@admin.register(Guard)
class GuardAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'device_info']

    def device_info(self, obj):
        return mark_safe('<a target="_blank" class="button" href="/admin/dashboard/device/{device_id}/change/"> Device Details </a>'.format(device_id=obj.device.id))
    device_info.allow_tags = True
    device_info.short_description = 'Device Info/Deployed Position'

    list_filter = ('client', 'device')
