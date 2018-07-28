from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import time
import threading


async_mode = "threading"


def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)


def single_device(request, device_id):
    context = {
        device_id: device_id,
    }
    thread = threading.Thread(name='device_monitoring',
                             target=single_device_monitor_call)
    thread.daemon = True
    thread.start()

    return render(request, 'dashboard/single_device.html', context=context)



def single_device_monitor_call():
    
    class TestNamespace(BaseNamespace):
        pass
    
    socketIO = SocketIO(host='192.168.1.103', port=5000, Namespace=LoggingNamespace)
    device = socketIO.define(TestNamespace, '/test')

    def motion_response(mgs):
        print('motion_response: ', mgs)

    def vibration_response(mgs):
        print('vibration_response: ', mgs)

    def magnetic_response(mgs):
        print('magnetic_response: ', mgs)

    device.on('motion_response', motion_response)
    device.on('vibration_response', vibration_response)
    device.on('magnetic_response', vibration_response)


    time.sleep(0.3)
    socketIO.wait()
