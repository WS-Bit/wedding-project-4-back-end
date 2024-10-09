from django.urls import path
from .views import SongRequestsView, SongRequestDetailView

urlpatterns = [
    path('songrequests/', SongRequestsView.as_view(), name='song-requests'),
    path('songrequests/<int:pk>/', SongRequestDetailView.as_view(), name='song-request-detail'),
]