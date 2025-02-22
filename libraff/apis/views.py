from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import redirect

from books.serializers import *
from books.models import Book
from users.models import *
from users.serializers import *


__all__ = [
    'BookListAPIView', 'BookDetailAPIView',
    'BookLikeAPIView', 'BookDownloadAPIView',
    'BookSearchAPIView', 'UserListAPIView',
    'UserCommentListAPIView', 'BookCommentListAPIView',
    'LikedBookListAPIView', 'CommentLikeListAPIView',
    'RegisterAPIView', 'AddCommentToBook'   
]


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerUserRegisterDataSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Profile created successfully', 
                             'username': user.username,
                             'email': user.email
                            },
                            status=status.HTTP_201_CREATED
                        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountUpdateView(APIView):
    """
    API endpoint to update to user account .
    """
    permission_classes = [IsAuthenticated] 
    
    def patch(self, request):
        user = request.user
        serializer = CustomerUserAccountUpdateSerializer(user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookPagination(PageNumberPagination):
    page_size = 10


class BookListAPIView(APIView):
    """
    API endpoint to retrieve a list of books or add a new book.
    """
    pagination_class = BookPagination

    def get(self, request):
        books = Book.objects.all().order_by('-like')
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(books, request)

        serializer = BookSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = CreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """
    API endpoint to retrieve, update, or delete a book by its ID.
    """
    permission_classes = [IsAuthenticated] 

    def get(self, request, book_id):
        if not request.user.is_authenticated:
            return redirect('/register/') 
        
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response({'detail': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookLikeAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, book_id):
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


class AddCommentToBook(APIView):
    """
    API endpoint to add a comment to a book.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        serializer = CommentSerializer(data=request.data)
        book = get_object_or_404(Book, id=book_id)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response({'message': 'Comment added succesfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

class BookDownloadAPIView(APIView):
    """
    API endpoint to download a book PDF by its ID.
    """
    permission_classes = [IsAuthenticated] 
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if book.pdf:
            response = FileResponse(book.pdf.open(), as_attachment=True, filename=f'{book.title}.pdf')
            return response
        return Response({'error': 'File not available'}, status=status.HTTP_400_BAD_REQUEST)


class BookSearchAPIView(APIView):
    """
    API endpoint to search books by title.
    """
    def get(self, request):
        query = request.query_params.get('query', '')
        books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class UserListAPIView(APIView):
    """
    API endpoint to retrieve all users.
    """
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        user = CustomerUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCommentListAPIView(APIView):
    """
    API endpoint to retrieve comments made by a specific user.
    """
    permission_classes = [IsAuthenticated] 
    def get(self, request, user_id):
        comment = Comments.objects.filter(id=user_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCommentListAPIView(APIView):
    """
    API endpoint to retrieve comments for a specific book.
    """
    permission_classes = [IsAuthenticated] 
    def get(self, request, book_id):
        comment = Comments.objects.filter(book_id=book_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikedBookListAPIView(APIView):
    """
    API endpoint to retrieve all liked books by user.
    """
    permission_classes = [IsAuthenticated] 
    def get(self, request, user_id):
        user = get_object_or_404(CustomerUser, id=user_id)
        liked_books = LikeBook.objects.filter(user=user)
        serializer = LikeBookSerializer(liked_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentLikeListAPIView(APIView):
    """
    API endpoint to retrieve all liked comments.
    """
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        comment = LikeComment.objects.all()
        serializer = LikeCommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
