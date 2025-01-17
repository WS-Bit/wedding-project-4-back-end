from django.core.management.base import BaseCommand
from rsvp.models import RSVP
from songrequests.models import SongRequest
from memories.models import Memories
from guests.models import Guest

class Command(BaseCommand):
    help = 'Cleans up all data from the database'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up database...')
        
        RSVP.objects.all().delete()
        self.stdout.write('Cleared RSVPs')
        
        SongRequest.objects.all().delete()
        self.stdout.write('Cleared Song Requests')
        
        Memories.objects.all().delete()
        self.stdout.write('Cleared Memories')
        
        Guest.objects.all().delete()
        self.stdout.write('Cleared Guests')
        
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up database'))