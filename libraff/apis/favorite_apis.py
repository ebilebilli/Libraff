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
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer


class OpenFavoriteListForUserAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, user_id):
        user = get_object_or_404(CustomerUser, id = user_id)
        favorites = Favorite.objects.filter(user=user, status=Favorite.OPEN).order_by('-created_at')
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'User_{user_id}_open_favorites_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
      
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(favorites, request)
        serializer = FavoriteSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)


class PrivateFavoriteListForUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnerOrAdminPermission]
    pagination_class = CustomPagination

    def get(self, request, user_id):
        user = get_object_or_404(CustomerUser, id = user_id)
        favorites = Favorite.objects.filter(user=user, status=Favorite.PRIVATE).order_by('-created_at')
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'User_{user_id}_private_favorites_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
      
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(favorites, request)
        serializer = FavoriteSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)


class FavoriteDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnerOrAdminPermission ]

    def get(self, request, favorite_id):
        user = request.user
        favorite = get_object_or_404(Favorite, id=favorite_id)
        cache_key = f'Favorite_detail_{favorite_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        if favorite.status == favorite.PRIVATE and favorite.user != user:
            return Response({'message': 'Authentication required for private favorites'}, status=status.HTTP_403_FORBIDDEN)

        if favorite.status == favorite.OPEN or favorite.user == user:
            serializer = FavoriteSerializer(favorite)
            cache.set(cache_key, serializer.data, timeout=CACHETIMEOUT)
            return Response(serializer.data, status=status.HTTP_200_OK) 


class CreateFavoriteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user = request.user
        serializer = FavoriteSerializer(data=request.data)
        book = get_object_or_404(Book, id=book_id)
        if Favorite.objects.filter(user=user, book=book).exists():
                return Response({'message': 'Already favorited'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save(user=user, book=book)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
  
class FavoriteManagementAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnerOrAdminPermission]

    def delete(self, request, favorite_id):
        user = request.user
        favorite = get_object_or_404(Favorite.objects.filter(user=user), id=favorite_id)
        favorite.delete()
        return Response({'message': 'Favorite deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
    def patch(self, request, favorite_id):
        user = request.user
        favorite = get_object_or_404(Favorite.objects.filter(user=user), id=favorite_id)
        serializer = FavoriteSerializer(favorite, data=request.data, partial=True)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

