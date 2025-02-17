from django.urls import path
from .views import *

app_name = 'apis'
urlpatterns = [path('books/', BookListAPIView.as_view(), name='books'),
               path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details'),
               path('search/',BookSearchAPIView.as_view(), name='book-search'),
               path('users/',UserListAPIView.as_view, name='users'),
               path('user/<int:user_id>/comments/',UserCommentListAPIView.as_view, name='user-comments'),
               path('book/<int:book_id>/comments/',BookCommentListAPIView.as_view, name='book-comments'),
               path('comment/likes/',CommentLikeListAPIView.as_view, name='comment-likes'),
               path('book/likes/',BookLikeListAPIView.as_view, name='book-likes'),


]
