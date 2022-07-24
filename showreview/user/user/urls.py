from django.urls import path, include
from .views import verify, register

urlpatterns = [
    path('verify/', verify),
    path('register/', register)
]