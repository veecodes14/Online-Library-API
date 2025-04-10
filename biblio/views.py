from django.http import JsonResponse
from .models import Biblio
from library.models import Borrow
from .serializers import BiblioSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics 
from rest_framework import filters

@api_view(['GET', 'POST'])
def biblio_list(request, format=None):

    if request.method == 'GET':
        biblio = Biblio.objects.all()
        serializer = BiblioSerializer(biblio, many=True)
        return Response(serializer.data) 
    
    if request.method == 'POST':
        serializer = BiblioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT', 'DELETE'])
def biblio_detail(request, id, format=None):

    try:
        biblio = Biblio.objects.get(pk=id)
    except Biblio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BiblioSerializer(biblio)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BiblioSerializer(biblio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        biblio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request, id):
    try:
        book = Biblio.objects.get(pk=id)
    except Biblio.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if not book.available:
        return Response({'error': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)

    # Mark book as borrowed
    Borrow.objects.create(user=request.user, book=book)
    book.available = False
    book.save()

    return Response({'message': f'You have successfully borrowed "{book.title}"'}, status=status.HTTP_200_OK)
    
class BiblioListAPIView(generics.ListAPIView):
    queryset = Biblio.objects.all()
    serializer_class = BiblioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'genre', 'published_date']
    ordering_fields = ['published_date']
    ordering = ['published_date']



