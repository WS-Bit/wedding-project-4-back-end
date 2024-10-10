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
        guest_id = request.data.get('guest_id')
        memory_text = request.data.get('memory_text')

        if not guest_id or not memory_text:
            return Response({'error': 'Both guest_id and memory_text are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            return Response({'error': 'Guest not found.'}, 
                            status=status.HTTP_404_NOT_FOUND)

        memory = Memories(guest=guest, memory_text=memory_text)
        memory.save()

        serializer = MemoriesSerializer(memory)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

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
    

class AllMemoriesView(APIView):
    def get(self, request):
        try:
            memories = Memories.objects.all()
            for memory in memories:
                print(memory.guest.name) 
            serializer = MemoriesSerializer(memories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


