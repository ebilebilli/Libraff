from rest_framework import serializers
from .models import Book, BookCategory

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() 
    class Meta:
        model = Book
        fields = '__all__'


class ChangeBookStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['status']