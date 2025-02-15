from rest_framework.views import APIView, Response, status
from books.serializers import *
from books.models import Book
from django.shortcuts import get_object_or_404


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
        book = get_object_or_404(Book, book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)