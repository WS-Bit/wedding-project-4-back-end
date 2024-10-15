from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from guests.models import Guest
from .models import SongRequest
from .serializers.common import SongRequestSerializer
from django.views.decorators.csrf import csrf_exempt

class SongRequestsView(APIView):
    @csrf_exempt
    def get(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        song_request = SongRequest.objects.filter(guest=guest).first()
        if song_request:
            serializer = SongRequestSerializer(song_request)
            return Response(serializer.data)
        else:
            return Response({"message": "No song request found for this guest"}, status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def post(self, request):
        guest_id = request.data.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        serializer = SongRequestSerializer(data=request.data, context={'guest': guest})
        if serializer.is_valid():
            serializer.save(guest=guest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def put(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        song_request = SongRequest.objects.filter(guest=guest).first()
        if not song_request:
            return Response({"error": "No song request found for this guest"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongRequestSerializer(song_request, data=request.data, context={'guest': guest})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        song_request = SongRequest.objects.filter(guest=guest).first()
        if not song_request:
            return Response({"error": "No song request found for this guest"}, status=status.HTTP_404_NOT_FOUND)

        song_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)