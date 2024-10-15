from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from guests.models import Guest
from .models import Memories
from .serializers.common import MemoriesSerializer
from django.views.decorators.csrf import csrf_exempt

class MemoryView(APIView):
    @csrf_exempt
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
    @csrf_exempt
    def post(self, request):
        serializer = MemoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MemoryDetailView(APIView):
    @csrf_exempt
    def get_object(self, pk, guest_id):
        try:
            memory = Memories.objects.get(pk=pk)
            if memory.guest.id != guest_id:
                raise PermissionDenied("You don't have permission to perform this action.")
            return memory
        except Memories.DoesNotExist:
            raise NotFound(detail="Memory not found")
    @csrf_exempt
    def delete(self, request, pk):
        guest_id = request.session.get('guest_id')
        if not guest_id:
            return Response({"error": "Guest not registered"}, status=status.HTTP_400_BAD_REQUEST)

        memory = self.get_object(pk, guest_id)
        memory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllMemoriesView(APIView):
    @csrf_exempt
    def get(self, request):
        try:
            memories = Memories.objects.all()
            for memory in memories:
                print(memory.guest.name) 
            serializer = MemoriesSerializer(memories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


