from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound
from guests.models import Guest
from .models import Memories
from .serializers.common import MemoriesSerializer

class MemoryView(APIView):
    def get(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        memories = Memories.objects.filter(guest=guest)
        serializer = MemoriesSerializer(memories, many=True)
        return Response(serializer.data)

    def post(self, request):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            raise NotFound(detail="Guest not found")

        serializer = MemoriesSerializer(data=request.data, context={'guest': guest})
        if serializer.is_valid():
            serializer.save(guest=guest)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MemoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Memories.objects.get(pk=pk)
        except Memories.DoesNotExist:
            raise NotFound(detail="Memory not found")

    def put(self, request, pk):
        memory = self.get_object(pk)
        serializer = MemoriesSerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        memory = self.get_object(pk)
        memory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)