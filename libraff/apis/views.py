from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from books.serializers import *
from books.models import Book
from users.models import *
from users.serializers import *

__all__ = [
    'BookListAPIView', 'BookDetailAPIView',
    'BookDownloadAPIView','LogoutAPIView',
    'BookSearchAPIView', 'UserListAPIView',
    'UserCommentListAPIView', 'LikedBookListAPIView',
    'CommentLikeListAPIView', 'RegisterAPIView',
    'CommentManagementAPIView', 'AccountDetailAPIView',
    'LoginAPIView', 
]

class HeHasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff

class Pagination(PageNumberPagination):
    """Custom pagination class with default page size of 10."""
    page_size = 10

class RegisterAPIView(APIView):
    """APIView for user registration."""

    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new user."""
        serializer = CustomerUserRegisterDataSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Profile created successfully',
                'username': user.username,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        if token:
            token.delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'No active account found'}, status=status.HTTP_400_BAD_REQUEST)

class BookListAPIView(APIView):
    """APIView for listing and creating books."""
    pagination_class = Pagination

    def get(self, request):
        """Retrieve a paginated list of all books sorted by likes."""
        books = Book.objects.all().order_by('-like')
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Create a new book."""
        serializer = CreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    """APIView for retrieving, updating, or deleting a specific book."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        """Retrieve details of a specific book by ID."""
        if not request.user.is_authenticated:
            return redirect('/register/')
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def post(self, request, book_id):
        """Like or unlike a specific book."""
        book = get_object_or_404(Book, id=book_id)
        user = request.user
        like_instance = LikeBook.objects.filter(user=user, book=book).first()

        if like_instance:
            like_instance.delete()
            book.like = max(0, book.like - 1)
            book.save()
            return Response({'detail': 'Like removed'}, status=status.HTTP_200_OK)

        LikeBook.objects.create(user=user, book=book)
        book.like += 1
        book.save()
        return Response({'detail': "Book liked"}, status=status.HTTP_200_OK)

class CommentManagementAPIView(APIView):
    """APIView for adding and retrieving comments for a specific book."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = Pagination

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
        comment = Comments.objects.filter(book_id=book_id)
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(comment, request)
        if comment.exists():
            serializer = CommentSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There is no any comment yet'}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        if comment:
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'There is not such message'}, status=status.HTTP_400_BAD_REQUEST)

class BookDownloadAPIView(APIView):
    """APIView for downloading book PDFs."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        """Download the PDF of a specific book."""
        book = get_object_or_404(Book, id=book_id)
        if book.pdf:
            response = FileResponse(book.pdf.open(), as_attachment=True, filename=f'{book.title}.pdf')
            return response
        return Response({'error': 'File not available'}, status=status.HTTP_400_BAD_REQUEST)

class BookSearchAPIView(APIView):
    """APIView for searching books by title."""
    pagination_class = Pagination

    def get(self, request):
        """Retrieve a paginated list of books matching the search query."""
        query = request.query_params.get('query', '')
        books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(books, request)
        if books.exists():
            serializer = BookSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There is not such book'}, status=status.HTTP_204_NO_CONTENT)

class UserListAPIView(APIView):
    """APIView for listing all users."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request):
        """Retrieve a paginated list of all users."""
        pagination = self.pagination_class()
        user = CustomerUser.objects.all()
        result_page = pagination.paginate_queryset(user, request)
        if user.exists():
            serializer = UserSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'No users found'}, status=status.HTTP_204_NO_CONTENT)

class AccountDetailAPIView(APIView):
    """APIView for retrieving and updating user account details."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, user_id):
        """Retrieve details of a specific user."""
        user = get_object_or_404(CustomerUser, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        """Partially update a specific user's account."""
        user = get_object_or_404(CustomerUser, id=user_id)
        self.check_object_permissions(request, user)

        serializer = CustomerUserAccountUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCommentListAPIView(APIView):
    """APIView for retrieving comments by a specific user."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, user_id):
        """Retrieve a paginated list of comments made by a specific user."""
        pagination = self.pagination_class()
        comment = Comments.objects.filter(user=user_id)
        if comment.exists():
            result_page = pagination.paginate_queryset(comment, request)
            serializer = CommentSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'No comments found'}, status=status.HTTP_204_NO_CONTENT)

class LikedBookListAPIView(APIView):
    """APIView for retrieving books liked by a specific user."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, user_id):
        """Retrieve a paginated list of books liked by a specific user."""
        user = get_object_or_404(CustomerUser, id=user_id)
        liked_books = LikeBook.objects.filter(user=user)
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(liked_books, request)
        serializer = LikeBookSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)

class CommentLikeListAPIView(APIView):
    """APIView for retrieving all liked comments."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get(self, request):
        """Retrieve a paginated list of all liked comments."""
        comment = LikeComment.objects.all()
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(comment, request)
        serializer = LikeCommentSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)
