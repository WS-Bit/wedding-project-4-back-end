# guests/urls.py

from django.urls import path
from .views import GuestView

urlpatterns = [
    path('', GuestView.as_view(), name='guests'),
]