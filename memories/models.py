from django.db import models
from guests.models import Guest
from django.utils import timezone

class Memories(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    memory_text = models.TextField()
    date_shared = models.DateField(default=timezone.now)  # Changed to DateField

    def __str__(self):
        return f"{self.guest.name}'s memory"