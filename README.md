📚 **Book Library API**
A Django REST Framework based API for managing books, user profiles, comments, and likes. Users can search, download books, and interact through likes and comments.

🚀 **Features**

### Book Management:
- List, retrieve, create, update, and delete books.
- Like/unlike books.
- Download books as PDFs.
- Search books by title.

### User Management:
- Register new users.
- Update user profiles.
- List all users.

### Comment System:
- Add comments to books.
- View comments by users and books.
- Like/unlike comments.

🛠️ **Technologies Used**
- Django (Python Web Framework)
- Django REST Framework (API Development)
- SQLite/PostgreSQL (Database)

📄 **Installation & Setup**

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

---

### 📊 **API Endpoints**

| Category                 | Method | Endpoint                          | Description                            | Authentication Required |
|--------------------------|--------|-----------------------------------|----------------------------------------|-------------------------|
| **Authentication**       | POST   | /login/                           | Obtain auth token                      | No                      |
|                          | POST   | /register/                        | Register a new user                    | No                      |
| **Book Management**      | GET    | /books/                           | List all books (paginated)             | No                      |
|                          | POST   | /books/                           | Add a new book                         | Yes                     |
|                          | GET    | /book/<book_id>/                  | Retrieve book details                  | Yes                     |
|                          | PUT    | /book/<book_id>/                  | Update book completely                 | Yes                     |
|                          | PATCH  | /book/<book_id>/                  | Partially update book                  | Yes                     |
|                          | DELETE | /book/<book_id>/                  | Delete a book                          | Yes                     |
|                          | POST   | /book/<book_id>/like/             | Like/unlike a book                     | Yes                     |
|                          | GET    | /book/<book_id>/download/         | Download book PDF                      | Yes                     |
|                          | GET    | /books/search/?query=<str>        | Search books by title                  | No                      |
| **User Management**      | GET    | /users/                           | List all users (paginated)             | Yes                     |
|                          | GET    | /user/<user_id>/                  | Get user details                       | Yes                     |
|                          | PATCH  | /user/<user_id>/                  | Update user profile                    | Yes                     |
|                          | GET    | /user/<user_id>/comments/         | List user's comments                   | Yes                     |
|                          | GET    | /user/<user_id>/liked_books/      | List user's liked books                | Yes                     |
| **Comment Management**   | GET    | /book/<book_id>/comments/         | List book comments (paginated)         | Yes                     |
|                          | POST   | /book/<book_id>/comments/         | Add comment to a book                  | Yes                     |
|                          | GET    | /comment/likes/                   | List all liked comments                | Yes                     |

---

### 📘 **Models**

#### **Book Model**

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

#### **User Model**

```python
class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    bio = models.TextField(max_length=550, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
```

#### **Comment Model**

```python
class Comments(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
```

📜 **License**
This project is licensed under the MIT License.

👨‍💻 **Author**
Developed by Abil Abilli 🚀

