from django.urls import path
from .views import *

app_name = 'apis'
urlpatterns = [path('books/', BookListAPIView.as_view(), name='books'),
               path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details'),
               path('book/<int:book_id>/like', BookLikeAPIView.as_view(), name='book-like'),
               path('book/<int:book_id>/download', BookLikeAPIView.as_view(), name='book-download'),
               path('books/search/', BookSearchAPIView.as_view(), name='book-search'),
               path('users/', UserListAPIView.as_view, name='users'),
               path('user/<int:user_id>/comments/', UserCommentListAPIView.as_view, name='user-comments'),
               path('book/<int:book_id>/comments/', BookCommentListAPIView.as_view, name='book-comments'),
               path('comment/likes/', CommentLikeListAPIView.as_view, name='comment-likes'),
               path('book/likes/', BookLikeListAPIView.as_view, name='book-likes'),


]
