from django.urls import path
from .views import MemoryView, MemoryDetailView

urlpatterns = [
    path('', MemoryView.as_view(), name='memory'),
    path('memories/<int:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
]