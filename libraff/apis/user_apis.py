from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from django.core.cache import cache

from libraff.settings import CACHETIMEOUT
from utils.custom_pagination import CustomPagination
from users.models import CustomerUser
from users.serializers import (
    CustomerUserSerializer,
    RegisterSerializer,
    AccountUpdateSerializer,
    LoginSerializer,
)


class RegisterAPIView(APIView):
    """API view for user registration."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle user registration."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'message': 'Profile created successfully',
                    'username': user.username,
                    'email': user.email,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """API view for user login."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user login."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """API view for user logout."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle user logout."""
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {'message': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserListAPIView(APIView):
    """API view for listing users."""
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        """Get paginated list of users."""
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'User_list_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        try:
            pagination = self.pagination_class()
            user = CustomerUser.objects.all()
            result_page = pagination.paginate_queryset(user, request)
            serializer = CustomerUserSerializer(result_page, many=True)
            paginated_response = pagination.get_paginated_response(
                serializer.data,
            ).data
            cache.set(cache_key, paginated_response, timeout=CACHETIMEOUT)
            return Response(
                paginated_response,
                status=status.HTTP_200_OK,
            )
        except CustomerUser.DoesNotExist:
            return Response(
                {'message': 'Users not found'},
                status=status.HTTP_404_NOT_FOUND,
            )


class AccountDetailAPIView(APIView):
    """API view for user account details."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """Get user details."""
        cache_key = f'User_detail_{user_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        user = get_object_or_404(CustomerUser, id=user_id)
        serializer = CustomerUserSerializer(user)
        cache.set(cache_key, serializer.data, timeout=CACHETIMEOUT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        """Update user account details."""
        user = get_object_or_404(CustomerUser, id=user_id)
        if user.id != request.user.id:
            return Response(
                {'message': 'You do not have permission'},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        serializer = AccountUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


