from rest_framework import serializers
from .models import Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.CharField(source='like_count')
    
    class Meta:
        model = Comment
        fields = [ 'content', 'created_at', 'user_name']
        read_only_fields = ['created_at', 'user', 'book', 'user_name']
        

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

