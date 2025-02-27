from rest_framework import serializers
from .models import Book, BookCategory

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        filds = '__all__'


class BookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() 
    class Meta:
        model = Book
        fields = '__all__'


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['id']