from django.contrib import admin
from django.urls import path, include
from .views import EnterPasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/enter_password/', EnterPasswordView.as_view(), name='enter_password'),
    path('api/guests/', include('guests.urls')),
    path('api/rsvp/', include('rsvp.urls')),
    path('api/songrequests/', include('songrequests.urls')),
    path('api/memories/', include('memories.urls')),
]