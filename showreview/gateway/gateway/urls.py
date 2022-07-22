from django.conf.urls import include, url
from .views import Routing

urlpatterns = [
    url(r'.*', Routing.as_view())
]