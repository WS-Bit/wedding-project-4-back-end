from django.urls import path
from .views import RSVPView

urlpatterns = [
    path('rsvp/', RSVPView.as_view()),
]