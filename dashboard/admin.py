from django.contrib import admin
from .models import Device, Client

from django.urls import reverse
from django.utils.html import mark_safe
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_code_name', 'client_name', 'device_ip_port',
                    'position_address', 'position_map', 'action_button']
    
    def device_ip_port(self, obj):
        return '{protocol}://{ip}:{port}'.format(protocol = obj.protocol, ip = obj.device_ip, port = obj.device_port)
    device_ip_port.short_description = 'Device IP Port Address'
    device_ip_port.allow_tags = True
    
    def action_button(self, obj):
        return mark_safe('<a target="_blank" class="button" href="/device_monitor/{device_id}"> Monitor This Device Now </a>'.format(device_id=obj.id))
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
