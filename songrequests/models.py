from django.db import models
from guests.models import Guest

class SongRequest(models.Model):
    def __str__(self):
        return f'Song request for {self.guest.name}'
    guest = models.OneToOneField(Guest, on_delete=models.CASCADE, related_name='song_request')
    song_title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)