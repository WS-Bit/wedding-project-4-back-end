from django.db import models
from guests.models import Guest

WEDDING_CHOICES = [
    ('ENG', 'England'),
    ('AUS', 'Australia'),
    ('BOTH', 'Both')
]

class RSVP(models.Model):
    def __str__(self):
        return f'RSVP for {self.guest.name}'
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='rsvp_response')
    wedding_selection = models.CharField(max_length=10, choices=WEDDING_CHOICES)
    is_attending = models.BooleanField(default=False)
    additional_notes = models.TextField(blank=True, null=True)