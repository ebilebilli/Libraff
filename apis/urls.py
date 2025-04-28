from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .user_apis import *
from .book_apis import *
from .interaction_apis import *


app_name = 'apis'

urlpatterns = [
    #User endpoints:
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('users/', UserListAPIView.as_view(), name='users'),
    path('users/search/', UserSearchAPIView.as_view(), name='user-search'),
    path('user/<int:user_id>/', AccountDetailAPIView.as_view(), name='user-account'),
    path('user/<int:user_id>/comments/', UserCommentListAPIView.as_view(), name='user-comments'),
    path('comment/likes/', LikedCommentListAPIView.as_view(), name='comment-likes'), 
     path('user/<int:user_id>/liked_books/', LikedBookListAPIView.as_view(), name='user-liked-books'),

    #Book endpoints:
    path('categories/', BookCategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:category_id>/books/', BookListForCategoryAPIView.as_view(), name='category-books'),
    path('books/', BookListAPIView.as_view(), name='books'),
    path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details'),
    path('book/<int:book_id>/comments/', CommentManagementAPIView.as_view(), name='comment-management'),
    path('book/<int:book_id>/download/', BookDownloadAPIView.as_view(), name='download-book'),
    path('books/search/', BookSearchAPIView.as_view(), name='book-search'),
    path('books/filter/', BookFilterAPIView.as_view(), name='book-filter'),

    #JWT endpoints: 
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
               
]
