from django.conf.urls import url
from django.urls import include

from apps.api.ping.urls import ping_urlpatterns

urlpatterns = [
    url('', include(ping_urlpatterns)),
    url('', include(reporter_urlpatterns)),
]
