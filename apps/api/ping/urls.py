from django.conf.urls import url

from apps.api.ping.views import ping

ping_urlpatterns = [
    url('ping', ping, name='ping'),
]
