from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction

from utils.custom_pagination import CustomPagination
from utils.permission_control import HeHasPermission
from books.models import Book
from users.models import CustomerUser
from interactions.models import Comment, Like
from interactions.serializers import CommentSerializer, LikeSerializer


class CommentManagementAPIView(APIView):
    """APIView for adding and retrieving comments for a specific book."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def post(self, request, book_id):
        """Add a comment to a specific book."""
        serializer = CommentSerializer(data=request.data)
        book = get_object_or_404(Book, id=book_id)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response({'message': 'Comment added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, book_id):
        """Retrieve a paginated list of comments for a specific book."""
        comment = Comment.objects.filter(book_id=book_id)
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(comment, request)
        if comment.exists():
            serializer = CommentSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There is no any comment yet'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment:
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'There is not such message'}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikedBookListAPIView(APIView):
    """APIView for retrieving books liked by a specific user."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, user_id):
        """Retrieve a paginated list of books liked by a specific user."""
        user = get_object_or_404(CustomerUser, id=user_id)
        liked_books = Like.objects.filter(user=user)
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(liked_books, request)
        serializer = LikeSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)


class LikedCommentListAPIView(APIView):
    """APIView for retrieving all liked comments."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        """Retrieve a paginated list of all liked comments."""
        comment = Like.objects.all()
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(comment, request)
        serializer = LikeSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)
