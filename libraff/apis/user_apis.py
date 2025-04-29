from rest_framework.views import APIView, Response, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.db import transaction

from utils.custom_pagination import CustomPagination
from utils.permission_control import OwnerOrAdminPermission
from users.models import *
from users.serializers import *



class RegisterAPIView(APIView):
    """APIView for user registration."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new user."""
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
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
    """
    User login API.

    POST: Accepts credentials and returns a token on success.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    User logout API.

    POST: Logs out the user by deleting the token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        if token:
            token.delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'No active account found'}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(APIView):
    """APIView for searching users by title."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        """Retrieve a paginated list of user matching the search query."""
        query = request.query_params.get('query', '')
        users = CustomerUser.objects.filter(username__icontains=query) if query else CustomerUser.objects.all()
        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(users, request)
        if users.exists():
            serializer = CustomerUser(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There is not such user'}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(APIView):
    """APIView for listing all users."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        """Retrieve a paginated list of all users."""
        pagination = self.pagination_class()
        user = CustomerUser.objects.all()
        result_page = pagination.paginate_queryset(user, request)
        if user.exists():
            serializer = CustomerUserSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'No users found'}, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailAPIView(APIView):
    """APIView for retrieving and updating user account details."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OwnerOrAdminPermission]

    def get(self, request, user_id):
        """Retrieve details of a specific user."""
        user = get_object_or_404(CustomerUser, id=user_id)
        serializer = CustomerUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        """Partially update a specific user's account."""
        user = get_object_or_404(CustomerUser, id=user_id)
        self.check_object_permissions(request, user)

        serializer = AccountUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


