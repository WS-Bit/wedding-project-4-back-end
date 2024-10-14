from django.contrib import admin
from django.urls import path, include
from .views import enter_password
from .views import set_csrf_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/enter_password/', enter_password.as_view(), name='enter_password'),
    path('api/csrf_cookie/', set_csrf_token, name='set_csrf_token'),
    path('api/guests/', include('guests.urls')),
    path('api/rsvp/', include('rsvp.urls')),
    path('api/songrequests/', include('songrequests.urls')),
    path('api/memories/', include('memories.urls')),
]