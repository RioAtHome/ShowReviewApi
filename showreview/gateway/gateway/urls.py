from django.urls import path, re_path
from .views import Routing

urlpatterns = [
    re_path(r"^", Routing.as_view()),
]
