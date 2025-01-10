# Django Authentication System

A robust Django web application that implements a complete authentication system with user registration, login, logout, and profile management functionalities.

## Features

- 👤 User Authentication
  - Registration with email verification
  - Login/Logout functionality
  - Password reset capability
  - Password change for logged-in users
  - Remember me functionality

- 🔒 Security Features
  - JWT (JSON Web Token) authentication
  - Password hashing
  - CSRF protection
  - Session management
  - Rate limiting for API endpoints

- 🎨 Frontend
  - Clean and responsive UI using Bootstrap 5
  - Custom form styling with crispy-forms
  - User-friendly error messages
  - Loading states and animations

- 🛠️ API Features
  - RESTful API endpoints
  - Token-based authentication
  - API documentation with swagger/OpenAPI
  - CORS support for cross-origin requests

## Technology Stack

- **Backend**: Django 5.0
- **Frontend**: Bootstrap 5, Crispy Forms
- **Database**: SQLite (default), PostgreSQL (production-ready)
- **Authentication**: django-allauth, JWT
- **API**: Django REST Framework
- **Security**: django-cors-headers

## Project Structure

```
auth/
├── auth/                   # Main project directory
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
│
├── base/                   # Main application
│   ├── templates/         # HTML templates
│   │   ├── base.html     # Base template
│   │   ├── home.html     # Home page
│   │   └── auth/         # Authentication templates
│   ├── static/           # Static files (CSS, JS, images)
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # App URL configuration
│   └── forms.py          # Form definitions
│
├── requirements.txt       # Project dependencies
├── .gitignore            # Git ignore file
└── manage.py             # Django management script
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/fahad0samara/django-auth.git
cd django-auth
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

- `/api/auth/register/` - User registration
- `/api/auth/login/` - User login
- `/api/auth/logout/` - User logout
- `/api/auth/password/reset/` - Password reset
- `/api/auth/password/change/` - Password change
- `/api/auth/user/` - User profile

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- All passwords are hashed using Django's password hasher
- CSRF protection is enabled
- JWT tokens are used for API authentication
- Rate limiting is implemented on sensitive endpoints
- Environment variables are used for sensitive data

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Fahad - [@your_twitter](https://twitter.com/your_twitter)

Project Link: [https://github.com/fahad0samara/django-auth](https://github.com/fahad0samara/django-auth)
