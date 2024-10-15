from django.contrib import admin
from django.urls import path, include
from jwt_auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/enter_password/', views.enter_password, name='enter_password'),
    path('api/auth/status/', views.auth_status, name='auth_status'),
    path('api/guests/', include('guests.urls')),
    path('api/rsvp/', include('rsvp.urls')),
    path('api/songrequests/', include('songrequests.urls')),
    path('api/memories/', include('memories.urls')),
]