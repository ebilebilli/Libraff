from django.urls import path
from .views import *


app_name = 'apis'
urlpatterns = [path('login/', LoginAPIView.as_view(), name='login'),
               path('logout/', LogoutAPIView.as_view(), name='logout'),
               path('register/', RegisterAPIView.as_view(), name='register'),
               path('books/', BookListAPIView.as_view(), name='books'),
               path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details'),
               path('book/<int:book_id>/comments/', CommentManagementAPIView.as_view(), name='comment-management'),
               path('book/<int:book_id>/download/', BookDownloadAPIView.as_view(), name='download-book'),
               path('books/search/', BookSearchAPIView.as_view(), name='book-search'),
               path('users/', UserListAPIView.as_view(), name='users'),
               path('user/<int:user_id>/', AccountDetailAPIView.as_view(), name='user-account'),
               path('user/<int:user_id>/comments/', UserCommentListAPIView.as_view(), name='user-comments'),
               path('comment/likes/', CommentLikeListAPIView.as_view(), name='comment-likes'), 
               path('user/<int:user_id>/liked_books/', LikedBookListAPIView.as_view(), name='user-liked-books')
               
]
