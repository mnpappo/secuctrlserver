from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('device_monitor/<int:device_id>', views.single_device, name='single_device'),
]

from django.conf import settings
from django.conf.urls import include, url

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
