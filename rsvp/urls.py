from django.urls import path
from .views import RSVPView

urlpatterns = [
    path('', RSVPView.as_view()),
]