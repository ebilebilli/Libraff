from django.urls import path
from .views import *

app_name = 'apis'
urlpatterns = [path('books/', BookListAPIView.as_view(), name='books'),
               path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details'),
               path('book/delete/<int:book_id>/', BookDeleteAPIView.as_view(), name='book-delete'),
               path('book/update/<int:book_id>/', BookUpdateAPIView.as_view(), name='book-update')
     
]