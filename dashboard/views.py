import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from datetime import date

from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import socketio

from .models import *



def send_sms(text, from_number='+12766018359', to='+8801821081270'):
    from twilio.rest import Client
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC38a5c8b35d68abae9d17f53faea79f81'
    auth_token = '885f0596dd532d9d8bb0403d47170325'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=text,
        from_=from_number,
        to=to
    )
    print(message.sid)
    return message.sid


async_mode = "threading"


basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)
thread = None


@sio.on('connect', namespace='/test')
def test_connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected',
                             'count': 0}, room=sid, namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


@sio.on('my_event', namespace='/test')
def test_message(sid, message):
    sio.emit('my_response', {
             'data': message['data']}, room=sid, namespace='/test')


def index(request):
    devices = Device.objects.all().values()
    number_of_devices = Device.objects.all().count()
    number_of_clients = Client.objects.all().count()
    number_of_guards = Guard.objects.all().count()
    number_of_active = Device.objects.filter(device_status="active").count()
    number_of_inactive = Device.objects.filter(device_status="inactive").count()
    todays_total_log = NotificationLog.objects.filter(notification_time__date=date.today()).count()
    todays_total_monitor = NotificationLog.objects.filter(notification_time__date=date.today(), notification_status='monitor').count()
    todays_total_warning = NotificationLog.objects.filter(notification_time__date=date.today(), notification_status='warning').count()
    todays_total_false = NotificationLog.objects.filter(notification_time__date=date.today(), notification_status='false').count()
    todays_total_intrusion = NotificationLog.objects.filter(notification_time__date=date.today(), notification_status='intrusion').count()
    print(number_of_devices)
    data = serializers.serialize( 'json', Device.objects.all(), fields=('device_code_name', 'position_address', 'device_ip', 'device_port', 'lattitude', 'longitude', 'device_status'))

    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)

    # chart maker
    # notification_chart = chart_maker()

    return render(request, 'dashboard/index.html', {
        'devices': data, 
        'number_of_devices': number_of_devices, 
        'number_of_clients': number_of_clients, 
        'number_of_guards': number_of_guards,
        'number_of_active': number_of_active,
        'number_of_inactive': number_of_inactive,
        'todays_total_log': todays_total_log,
        'todays_total_monitor': todays_total_monitor,
        'todays_total_warning': todays_total_warning,
        'todays_total_false': todays_total_false,
        'todays_total_intrusion': todays_total_intrusion,
        })


def background_thread():
    class TestNamespace(BaseNamespace):
        pass

    socketIO = SocketIO(host='192.168.1.106', port=5000,
                        Namespace=LoggingNamespace)
    sioclient = socketIO.define(TestNamespace, '/test')

    def flame_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('flame'))
        n = NotificationLog(sensor_name='flame', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()
        mgs_text = 'Fire Alarm!!!!!!!!! \n Device Name: ' + \
            str(device.name) + '\n Notification Time: ' + str(mgs.get('time'))
        # send_sms(mgs_text)
        print('flame_response: ', mgs)
        sio.emit('flame_response', mgs, namespace='/test')

    def temp_hum_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('hum')) + ',' + str(mgs.get('temp'))
        n = NotificationLog(sensor_name='temp_hum', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()
        print('temp_hum_response: ', mgs)
        sio.emit('temp_hum_response', mgs, namespace='/test')

    def motion_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('detected'))
        n = NotificationLog(sensor_name='motion', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()

        print('motion_response: ', mgs)
        sio.emit('motion_response', mgs, namespace='/test')

    def vibration_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('detected'))
        n = NotificationLog(sensor_name='vibration', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()

        print('vibration_response: ', mgs)
        sio.emit('vibration_response', mgs, namespace='/test')

    def magnetic_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('state'))
        n = NotificationLog(sensor_name='magnetic_door', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()

        print('magnetic_response: ', mgs)
        sio.emit('magnetic_response', mgs, namespace='/test')

    def siren_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('state'))
        n = NotificationLog(sensor_name='panic', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()

        print('siren_response: ', mgs)
        sio.emit('siren_response', mgs, namespace='/test')

    def attend_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('state'))
        n = NotificationLog(sensor_name='attendance', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()

        print('attend_response: ', mgs)
        sio.emit('attend_response', mgs, namespace='/test')

    def laser_response(mgs):
        device = Device.objects.get(pk=1)
        sensor_value = str(mgs.get('state'))
        n = NotificationLog(sensor_name='laser', sensor_value=sensor_value,
                            device=device, notification_time=mgs.get('time'))
        n.save()

        print('laser_response: ', mgs)
        sio.emit('laser_response', mgs, namespace='/test')

    sioclient.on('flame_response', flame_response)
    sioclient.on('temp_hum_response', temp_hum_response)
    sioclient.on('motion_response', motion_response)
    sioclient.on('vibration_response', vibration_response)
    sioclient.on('magnetic_response', magnetic_response)
    sioclient.on('siren_response', siren_response)
    sioclient.on('attend_response', attend_response)
    sioclient.on('laser_response', laser_response)

    socketIO.wait()


def all_notification(request):
    context = {}
    return render(request, 'dashboard/notifications.html', context)
