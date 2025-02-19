# Book Library API

## Overview
The **Book Library API** is a Django-based backend system that allows users to interact with books by downloading, liking, and commenting on them. Additionally, users can like comments and manage their profiles.

## Features
- List all books
- Retrieve details of a specific book
- Like a book
- Download a book
- Search for books
- List all users
- Retrieve comments by a user
- Retrieve comments on a book
- Like a comment
- View all liked books

## Technologies Used
- **Django** (Python Web Framework)
- **Django REST Framework** (API Development)
- **SQLite/PostgreSQL** (Database)

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd book-library-api
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # For Mac/Linux
   env\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (optional for admin access):
   ```sh
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Book Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/books/` | List all books |
| `POST` | `/books/` | Add a new book |
| `GET` | `/book/<book_id>/` | Get details of a specific book |
| `DELETE` | `/book/<book_id>/` | Delete a book |
| `PUT` | `/book/<book_id>/` | Update book details |
| `PATCH` | `/book/<book_id>/like` | Like a book |
| `GET` | `/book/<book_id>/download` | Download a book PDF |
| `GET` | `books/search/?query=<search_term>` | Search for books |

### User Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/users/` | List all users |
| `GET` | `/user/<user_id>/comments/` | Get comments by a user |

### Comment Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/book/<book_id>/comments/` | Get comments for a book |
| `GET` | `/comment/likes/` | List all liked comments |
| `GET` | `/book/likes/` | List all liked books |

## Models

### Book Model
```python
class Book(models.Model):
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    like = models.IntegerField(default=0)
    pdf = models.FileField(upload_to='books/pdf')

    def __str__(self):
        return f'{self.title}'
```

### User Model
```python
class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    bio = models.TextField(max_length=550, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
```

### Comment Model
```python
class Comments(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    context = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
```

## License
This project is open-source and available under the **MIT License**.

## Author
Developed by **Abil Abilli** 🚀

