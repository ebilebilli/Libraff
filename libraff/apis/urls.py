from django.urls import path
from .views import *

app_name = 'apis'
urlpatterns = [path('books/', BookListAPIView.as_view(), name='books'),
               path('book/<int:book_id>/', BookDetailAPIView.as_view(), name='book-details')
     
]