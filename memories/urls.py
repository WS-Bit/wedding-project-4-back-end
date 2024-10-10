from django.urls import path
from .views import MemoryView, MemoryDetailView, AllMemoriesView

urlpatterns = [
    path('', MemoryView.as_view(), name='memory'),
    path('<int:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
    path('all/', AllMemoriesView.as_view(), name='all-memories'),
]