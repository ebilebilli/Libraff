from rest_framework.views import APIView, Response, status
from books.serializers import *
from books.models import Book
from users.models import *
from users.serializers import *
from django.shortcuts import get_object_or_404

#Book App
class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = CreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  
class BookDetailAPIView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response({'detail': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#User App
class UserListAPIView(APIView):
    def get(self, request):
        user = CustomerUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCommentListAPIView(APIView):
    def get(self, request, user_id):
        comment = Comments.objects.filter(book_id=user_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCommentListAPIView(APIView):
    def get(self, request, book_id):
        comment = Comments.objects.filter(book_id=book_id)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookLikeListAPIView(APIView):
    def get(self, request):
        comment = LikeBook.objects.all()
        serializer = LikeBookSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentLikeListAPIView(APIView):
    def get(self, request):
        comment = LikeComment.objects.all()
        serializer = LikeCommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

