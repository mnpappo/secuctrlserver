"""
WSGI config for secuadminctl project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from socketio import Middleware
from dashboard.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secuadminctl.settings")

django_app = get_wsgi_application()
application = Middleware(sio, django_app)