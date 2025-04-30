from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .user_apis import *
from .book_apis import *
from .interaction_apis import *
from .favorite_apis import *

app_name = 'apis'

urlpatterns = [
    #User endpoints:
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('users/', UserListAPIView.as_view(), name='users'),
    path('user/<int:user_id>/', AccountDetailAPIView.as_view(), name='user-account'),

    #Book endpoints:
    path('categories/', BookCategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:category_id>/books/', BookListForCategoryAPIView.as_view(), name='category-books'),
    path('books/', BookListAPIView.as_view(), name='books'),
    path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('book/<int:book_id>/comments/', CommentManagementAPIView.as_view(), name='comment-management'),
    path('book/<int:book_id>/download/', BookDownloadAPIView.as_view(), name='download-book'),
    path('books/search/', BookSearchAPIView.as_view(), name='book-search'),
    path('books/filter/', BookFilterAPIView.as_view(), name='book-filter'),

    #Interaction endpoints:
    path('book/<int:book_id>/comments/', CommentsForBookAPIView.as_view(), name='comments-for-book'),
    path('book/<int:book_id>/comment/create/', CreateCommentAPIView.as_view(), name='create-comment'),
    path('book/<int:book_id>/comments/manage/', CommentManagementAPIView.as_view(), name='comment-management'),
    path('book/<int:comment_id>/comment/detail/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('user/<int:user_id>/comments/', CommentListForUserAPIView.as_view(), name='user-comments'),
    path('book/<int:book_id>/likes/', LikeListForBookAPIView.as_view(), name='likes-for-book'),
    path('comment/<int:comment_id>/likes/', LikeListForCommentAPIView.as_view(), name='likes-for-comment'),
    path('book/<int:book_id>/like/manage/', LikeManagementForBookAPIView.as_view(), name='like-management-for-book'),
    path('book/<int:comment_id>/like/manage/', LikeManagementForCommentAPIView.as_view(), name='like-management-for-comment'),

    #Favorite endpoints:
    path('user/<int:user_id>/favorites/open/', OpenFavoriteListForUserAPIView.as_view(), name='open-favorites-for-user'),
    path('user/<int:user_id>/favorites/private/', PrivateFavoriteListForUserAPIView.as_view(), name='open-favorites-for-user'),
    path('favorite/<int:favorite_id>/', FavoriteDetailAPIView.as_view(), name='favorite-detail'),
    path('book/<int:book_id>/favorite/create/', CreateFavoriteAPIView.as_view(), name='create-favorite'),
    path('favorite/<int:favorite_id>/manage/', FavoriteManagementAPIView.as_view(), name='favorite-management'),

    #JWT endpoints: 
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
               
]
