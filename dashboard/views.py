from django.shortcuts import render
from django.http import HttpResponse

# from socketio_client.manager import Manager
from socketIO_client import SocketIO, LoggingNamespace

import gevent
from gevent import monkey
monkey.patch_socket()

async_mode = "threading"

def temp_hum_response(args):
    print('\n\n\n\temp_hum_response', args)

def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)


socketIO = SocketIO('192.168.0.105', 5000, LoggingNamespace)
socketIO.on('temp_hum_response', temp_hum_response)
socketIO.emit('aaa')
socketIO.wait(seconds=1)
