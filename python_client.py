from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import time
import threading

# import logging
# logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
# logging.basicConfig()

socketIO = SocketIO('192.168.1.103', 5000, LoggingNamespace)


class TestNamespace(BaseNamespace):
    pass


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
