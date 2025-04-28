from rest_framework import serializers
from .models import Book, BookCategory, UserBookStatus


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    user_status = serializers.SerializerMethodField() 
    class Meta:
        model = Book
        fields = '__all__'
    
    def get_user_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            obj_status = UserBookStatus.objects.filter(user=request.user, book=obj).first()
            return obj_status.status if obj_status else UserBookStatus.UNREAD
        return UserBookStatus.UNREAD


class UserBookStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookStatus
        fields = ['status']
