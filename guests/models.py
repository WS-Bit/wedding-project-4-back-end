from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

DIETARY_CHOICES = [
    ('N/A', 'Not Applicable'),
    ('VEG', 'Vegetarian'),
    ('VGN', 'Vegan'),
    ('GF', 'Gluten-Free'),
    ('NUT', 'Nut-Free'),
    ('LAC', 'Lactose-Free'),
    ('SPE', 'Specific'), 
]


class Guest(models.Model):
  def __str__(self):
    return f'{self.name}'
  name = models.CharField(max_length=80, unique=True)
  email = models.CharField(max_length=50, unique=True)
  phone = PhoneNumberField()
  dietary_restrictions = models.CharField(max_length=3, choices=DIETARY_CHOICES)
  specific_dietary_restrictions = models.TextField(blank=True, null=True)