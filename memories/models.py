from django.db import models
from guests.models import Guest
from django.utils import timezone

class Memories(models.Model):
    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memories"
    def __str__(self):
        return f'Song request for {self.guest.name}'
    guest = models.OneToOneField(Guest, on_delete=models.CASCADE, related_name='memory')
    memory_text = models.CharField(max_length=100)
    date_shared = models.DateField(default=timezone.now)