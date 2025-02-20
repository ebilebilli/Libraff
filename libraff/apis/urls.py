from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'apis'
urlpatterns = [path('login/', obtain_auth_token, name='login'),
               path('register/', RegisterAPIView.as_view(), name='register'),
               path('books/', BookListAPIView.as_view(), name='books'),
               path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details'),
               path('book/<int:book_id>/like', BookLikeAPIView.as_view(), name='book-like'),
               path('book/<int:book_id>/download', BookDownloadAPIView.as_view(), name='book-download'),
               path('books/search/', BookSearchAPIView.as_view(), name='book-search'),
               path('users/', UserListAPIView.as_view(), name='users'),
               path('user/<int:user_id>/comments/', UserCommentListAPIView.as_view(), name='user-comments'),
               path('book/<int:book_id>/comments/', BookCommentListAPIView.as_view(), name='book-comments'),
               path('comment/likes/', CommentLikeListAPIView.as_view(), name='comment-likes'),
               path('user/<int:user_id>/liked_books/', LikedBookListAPIView.as_view(), name='user-liked-books')
               


]
