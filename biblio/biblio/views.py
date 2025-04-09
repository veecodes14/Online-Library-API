from django.http import JsonResponse
from .models import Biblio
from .serializers import BiblioSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 

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



