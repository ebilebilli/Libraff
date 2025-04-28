import hashlib
from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache  

from libraff.settings import CACHETIMEOUT
from utils.custom_pagination import CustomPagination
from books.models import Book, BookCategory, UserBookStatus
from books.serializers import BookSerializer, BookCategorySerializer, UserBookStatusSerializer


class BookCategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'Book_category_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        try:
            category = BookCategory.objects.all()
            serializer = BookCategorySerializer(category, many=True)
            cache.set(cache_key, serializer.data, timeout=CACHETIMEOUT)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BookCategory.DoesNotExist:
            return Response({'message': 'Categories not found'}, status=status.HTTP_404_NOT_FOUND)  


class BookListForCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, category_id):
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '10')
        cache_key = f'Book_list_for_category_{category_id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            category = get_object_or_404(BookCategory, id=category_id)
            books = Book.objects.filter(category=category).order_by('-created_at')
            pagination = self.pagination_class()
            result_page = pagination.paginate_queryset(books, request)
            serializer = BookSerializer(result_page, many=True)
            paginated_response = pagination.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
            return Response(paginated_response, status=status.HTTP_200_OK)
        except BookCategory.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)     


class BookListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'Book_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        try:
            books = Book.objects.all()
            serializer = BookCategorySerializer(books, many=True)
            cache.set(cache_key, serializer.data, timeout=CACHETIMEOUT)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'message': 'Books not found'}, status=status.HTTP_404_NOT_FOUND)  


class BookDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        user = request.user
        cache_key = f'Book_detail_{book_id}_user_{user.id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        try:
            book = get_object_or_404(Book, id=book_id)
            serializer = BookSerializer(book)
            cache.set(cache_key, serializer.data, timeout=CACHETIMEOUT)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({'message': 'Specified book does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, book_id):
        try:
            user = request.user
            book = get_object_or_404(Book, id=book_id)
            book_status = UserBookStatus.objects.get_or_create(user=user, book=book)
            serializer = UserBookStatusSerializer(book_status, data=request.data, partial=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'message': 'Specified book does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
   
class BookDownloadAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        try:
            book = get_object_or_404(Book, id=book_id)
            if not book.pdf:
                return Response({'message': 'File is not available'}, status=status.HTTP_400_BAD_REQUEST)
            
            response = FileResponse(book.pdf.open(), as_attachment=True, filename=f'{book.title}.pdf')
            return response
        except:
            return Response({'message': 'Specified book does not exist'}, status=status.HTTP_404_NOT_FOUND)  


class BookSearchAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        query = request.query_params.get('query', '')
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '10')
        cache_key = f'Book_search_query_{query}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
            pagination = self.pagination_class()
            result_page = pagination.paginate_queryset(books, request)
            serializer = BookSerializer(result_page, many=True)
            paginated_response = pagination.get_paginated_response(serializer.data).data
            cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
            return Response(paginated_response, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
             return Response({'message': 'Books not found'}, status=status.HTTP_404_NOT_FOUND)  


class BookFilterAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        pagination = self.pagination_class()
        data = request.query_params
        price_from = data.get('price_from')
        price_to = data.get('price_to')
        for_category = data.get('category')
        for_author = data.get('author')
        for_context = data.get('context')
        page = data.get('page', '1')
        page_size = data.get('page_size', '10')

        cache_key = hashlib.md5(
        (
        f'Book_filter_price_from_{price_from}_'
        f'price_to_{price_to}_'
        f'cat_{for_category}_'
        f'auth_{for_author}_'
        f'context_{for_context}_'
        f'page_{page}_'
        f'size_{page_size}'
        ).encode('utf-8')).hexdigest()
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        books = Book.objects.all()
        if price_from:
            books = books.filter(price__gte=price_from)
        if price_to:
            books = books.filter(price__lte=price_to)
        if for_category:
            books = books.filter(category__icontains=for_category)
        if for_author:
            books = books.filter(author__icontains=for_author)
        if for_context:
            books = books.filter(context__icontains=for_context)

        result_page = pagination.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)

