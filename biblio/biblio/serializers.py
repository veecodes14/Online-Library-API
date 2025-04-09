from rest_framework import serializers
from .models import Biblio

class BiblioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biblio
        fields = ['id', 'title', 'author', 'genre']