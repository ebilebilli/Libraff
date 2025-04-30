from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from django.core.cache import cache

from libraff.settings import CACHETIMEOUT
from utils.custom_pagination import CustomPagination
from utils.permission_control import OwnerOrAdminPermission
from books.models import Book
from users.models import CustomerUser
from interactions.models import Comment, Like
from interactions.serializers import CommentSerializer, LikeSerializer


#Comment views
class CommentsForBookAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, book_id):
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'Book_{book_id}_comments_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        comments = Comment.objects.filter(book_id=book_id)
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)


class CommentDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, comment_id):
        user = request.user
        cache_key = f'Comment_detail_{comment_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment)
        cache.set(cache_key, serializer.data, timeout=CACHETIMEOUT)
        return Response(serializer.data, status=status.HTTP_200_OK)        
            

class CreateCommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user = request.user
        serializer = CommentSerializer(data=request.data)
        book = get_object_or_404(Book, id=book_id)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save(user=user, book=book)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
  
class CommentManagementAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnerOrAdminPermission]

    def delete(self, request, comment_id):
        user = request.user
        comment = get_object_or_404(Comment.objects.filter(user=user), id=comment_id)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
    def patch(self, request, comment_id):
        user = request.user
        comment = get_object_or_404(Comment.objects.filter(user=user), id=comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListForUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnerOrAdminPermission]
    pagination_class = CustomPagination

    def get(self, request, user_id):
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'User_{user_id}_comments_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        pagination = self.pagination_class()
        user = get_object_or_404(CustomerUser, id=user_id)
        comment = Comment.objects.filter(user=user)
        result_page = pagination.paginate_queryset(comment, request)
        serializer = CommentSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)
      

#Like views
class LikeListForBookAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, book_id):
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'Likes_for_book_{book_id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        pagination = self.pagination_class()
        book = get_object_or_404(Book, id=book_id)
        likes = Like.objects.filter(book=book)
        like_count = likes.count()
        result_page = pagination.paginate_queryset(likes, request)
        serializer = LikeSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        paginated_response['like_count'] = like_count
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)
    

class LikeListForCommentAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, comment_id):
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'Likes_for_comment_{comment_id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        pagination = self.pagination_class()
        comment = get_object_or_404(Comment, id=comment_id)
        likes = Like.objects.filter(comment=comment)
        like_count = likes.count()
        result_page = pagination.paginate_queryset(likes, request)
        serializer = LikeSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        paginated_response['like_count'] = like_count
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)


class LikeManagementForBookAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        if Like.objects.filter(user=user, book=book).exists():
            return Response({'error': 'Already you liked this book'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            like = Like.objects.create(user=user, book=book)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, book_id):
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        like = Like.objects.filter(user=user, book=book).first()
        if like:
            like.delete()
            return Response({'message': 'Like deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)


class LikeManagementForCommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        user = request.user
        comment = get_object_or_404(Comment, id=comment_id)
        if Like.objects.filter(user=user, comment=comment).exists():
            return Response({'error': 'Already you liked this comment'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            like = Like.objects.create(user=user, comment=comment)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        user = request.user
        comment = get_object_or_404(Comment, id=comment_id)
        like = Like.objects.filter(user=user, comment=comment).first()
        if like:
            like.delete()
            return Response({'message': 'Like deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)

