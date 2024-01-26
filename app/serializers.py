from rest_framework import serializers

from .models import BookHolder


class BookHolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = BookHolder
        fields = ['name']

    
