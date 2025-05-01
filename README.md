# 📚 Libraff - Modern Book Management System

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-FF1709?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
</div>

## 🚀 Overview

Libraff is a modern, scalable book management system built with Django and Django REST Framework. It provides a comprehensive platform for managing and accessing books with advanced features like social interactions, user management, and performance optimizations.

## ✨ Key Features

### 📖 Book Management
- **Comprehensive Book Operations**
  - View detailed book information
  - Download books in PDF format
  - Advanced search and filtering
  - Book categorization system
  - Price range filtering
  - Author and context-based search

### 👥 User Experience
- **Authentication & Authorization**
  - JWT-based authentication
  - Secure user registration
  - Role-based access control
  - Profile management
  - Session management

### 💬 Social Features
- **Interactive Platform**
  - Comment system for books
  - Like/unlike functionality
  - Public and private favorites
  - User activity tracking
  - Social interactions

### ⚡ Performance
- **Optimized System**
  - Redis caching implementation
  - Custom pagination
  - Database query optimization
  - Asynchronous task processing
  - WebSocket support for real-time updates

## 🔧 Technical Stack

- **Backend Framework**: Django 5.1.6
- **API Framework**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL/SQLite
- **Caching**: Redis
- **Task Queue**: Celery
- **Real-time**: Django Channels
- **API Documentation**: DRF-YASG (Swagger/OpenAPI)

## 📡 API Documentation

### Authentication Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/register/` | POST | Register new user | No |
| `/api/auth/login/` | POST | User login | No |
| `/api/auth/logout/` | POST | User logout | Yes |

### User Management

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/users/` | GET | List all users | No |
| `/api/users/{user_id}/` | GET | Get user details | No |
| `/api/users/{user_id}/` | PATCH | Update user profile | Yes |

### Book Management

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/books/` | GET | List all books | No |
| `/api/books/{book_id}/` | GET | Get book details | No |
| `/api/books/{book_id}/` | PATCH | Update book status | Yes |
| `/api/books/category/{category_id}/` | GET | List books by category | No |
| `/api/books/search/` | GET | Search books | No |
| `/api/books/filter/` | GET | Filter books | No |
| `/api/books/{book_id}/download/` | GET | Download book | Yes |

### Comments System

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/books/{book_id}/comments/` | GET | List book comments | No |
| `/api/comments/{comment_id}/` | GET | Get comment details | No |
| `/api/books/{book_id}/comments/` | POST | Create comment | Yes |
| `/api/comments/{comment_id}/` | PATCH | Update comment | Yes |
| `/api/comments/{comment_id}/` | DELETE | Delete comment | Yes |

### Likes System

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/books/{book_id}/likes/` | GET | List book likes | No |
| `/api/books/{book_id}/likes/` | POST | Like book | Yes |
| `/api/books/{book_id}/likes/` | DELETE | Unlike book | Yes |
| `/api/comments/{comment_id}/likes/` | GET | List comment likes | No |
| `/api/comments/{comment_id}/likes/` | POST | Like comment | Yes |
| `/api/comments/{comment_id}/likes/` | DELETE | Unlike comment | Yes |

### Favorites System

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/users/{user_id}/favorites/open/` | GET | List public favorites | No |
| `/api/users/{user_id}/favorites/private/` | GET | List private favorites | Yes |
| `/api/favorites/{favorite_id}/` | GET | Get favorite details | Yes |
| `/api/books/{book_id}/favorites/` | POST | Add to favorites | Yes |
| `/api/favorites/{favorite_id}/` | PATCH | Update favorite | Yes |
| `/api/favorites/{favorite_id}/` | DELETE | Remove favorite | Yes |

## 🛠️ Query Parameters

### Pagination
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)

### Search
- `query`: Search term for book titles

### Filtering
- `price_from`: Minimum price
- `price_to`: Maximum price
- `category`: Filter by category
- `author`: Filter by author
- `context`: Filter by context

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL (optional)
- Redis
- Virtual environment

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/libraff.git
cd libraff
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up database**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Run Celery worker**
```bash
celery -A libraff worker -l info
```

9. **Run Redis server**
```bash
redis-server
```

## 🔐 Security Features

- JWT-based authentication
- Password hashing
- CSRF protection
- Rate limiting
- Input validation
- Secure file uploads
- Role-based access control

## 📊 Performance Optimizations

- Redis caching
- Database query optimization
- Pagination
- Lazy loading
- Asynchronous tasks
- Connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Your Name** - [@yourtwitter](https://twitter.com/yourtwitter)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- Django REST Framework team
- Redis community
- PostgreSQL team
- All contributors

---

