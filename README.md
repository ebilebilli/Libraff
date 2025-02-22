# 📚 Book Library API

A **Django REST Framework** based API for managing books, user profiles, comments, and likes. Users can search, download books, and interact through likes and comments.

## 🚀 Features

- **Book Management**:
  - List, retrieve, create, update, and delete books.
  - Like/unlike books.
  - Download books as PDFs.
  - Search books by title.

- **User Management**:
  - Register new users.
  - Update user profiles.
  - List all users.

- **Comment System**:
  - Add comments to books.
  - View comments by users and books.
  - Like/unlike comments.

## 🛠️ Technologies Used

- **Django** (Python Web Framework)
- **Django REST Framework** (API Development)
- **SQLite/PostgreSQL** (Database)

## 📄 Installation & Setup

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd book-library-api
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # Mac/Linux
   env\Scripts\activate    # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional for admin access):

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

## 📊 API Endpoints

### 📚 Book Endpoints

| Method   | Endpoint                  | Description             |
|----------|---------------------------|-------------------------|
| `GET`    | `/books/`                 | List all books          |
| `POST`   | `/books/`                 | Add a new book          |
| `GET`    | `/book/<book_id>/`        | Retrieve book details   |
| `PUT`    | `/book/<book_id>/`        | Update book details     |
| `PATCH`  | `/book/<book_id>/`        | Partially update book   |
| `DELETE` | `/book/<book_id>/`        | Delete a book           |
| `POST`   | `/book/<book_id>/like/`   | Like/unlike a book      |
| `GET`    | `/book/<book_id>/download`| Download book PDF       |
| `GET`    | `/books/search/?query=<>` | Search books by title   |

### 👤 User Endpoints

| Method   | Endpoint                  | Description              |
|----------|---------------------------|--------------------------|
| `POST`   | `/register/`              | Register a new user      |
| `PATCH`  | `/account/update/`        | Update user profile      |
| `GET`    | `/users/`                 | List all users          |

### 💬 Comment Endpoints

| Method   | Endpoint                      | Description                   |
|----------|-------------------------------|-------------------------------|
| `POST`   | `/book/<book_id>/comment/`    | Add a comment to a book       |
| `GET`    | `/user/<user_id>/comments/`   | Get comments by a user        |
| `GET`    | `/book/<book_id>/comments/`   | Get comments for a book       |
| `GET`    | `/comments/likes/`            | List all liked comments       |
| `GET`    | `/books/likes/`               | List all liked books          |

## 📚 Models

### Book Model
```python
class Book(models.Model):
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    like = models.IntegerField(default=0)
    pdf = models.FileField(upload_to='books/pdf')

    def __str__(self):
        return self.title
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

## 📜 License

This project is licensed under the **MIT License**.

## 👨‍💻 Author

Developed by **Abil Abilli** 🚀

