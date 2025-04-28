from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from books.models import BookCategory, Book


class BookCategoryModelTest(TestCase):
    def test_create_category(self):
        category = BookCategory.objects.create(category_name='Dram')
        self.assertEqual(category.category_name, 'Dram')
        self.assertEqual(str(category), 'Dram')
    
    def test_unique_category_name(self):
        category = BookCategory(category_name='')
        with self.assertRaises(ValidationError):
            category.full_clean()
            
          
    def test_book_and_category_relationship(self):
        category = BookCategory.objects.create(category_name='Sevgi')
        book = Book.objects.create(title='Icimizdeki Seytan', category=category)
        self.assertEqual(book.category, category)
        self.assertEqual(category.book_set.count(), 1)


class BookCategoryListAPITest(APITestCase):
    def setUp(self):
        self.category_one = BookCategory.objects.create(category_name='Dark Fantasy')
        self.category_two = BookCategory.objects.create(category_name='Science Fiction')
        self.url = '/api/v1/categories/'
    
    def test_get_book_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['category_name'], self.category_one.category_name)
        self.assertEqual(response.data[1]['category_name'], self.category_two.category_name)
    
    def test_no_book_categories(self):
        BookCategory.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)