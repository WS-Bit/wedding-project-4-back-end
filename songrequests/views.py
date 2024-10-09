from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from guests.models import Guest
from .models import SongRequest
from .serializers.common import SongRequestSerializer

class SongRequestsView(APIView):
    def get(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        song_requests = SongRequest.objects.filter(guest=guest)
        serializer = SongRequestSerializer(song_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        serializer = SongRequestSerializer(data=request.data, context={'guest': guest})
        if serializer.is_valid():
            serializer.save(guest=guest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongRequestDetailView(APIView):
    def get_object(self, pk, guest):
        try:
            return SongRequest.objects.get(pk=pk, guest=guest)
        except SongRequest.DoesNotExist:
            raise NotFound(detail="Song request not found")

    def put(self, request, pk):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        song_request = self.get_object(pk, guest)
        serializer = SongRequestSerializer(song_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        song_request = self.get_object(pk, guest)
        song_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)