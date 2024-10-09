from django.urls import path
from .views import SongRequestsView

urlpatterns = [
    path('', SongRequestsView.as_view()),
]