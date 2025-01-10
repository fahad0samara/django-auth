# Django Authentication Project

A Django web application that implements user authentication functionality.

## Project Structure

```
auth/
├── auth/               # Main project directory
│   ├── settings.py     # Project settings
│   ├── urls.py        # Main URL configuration
│   ├── asgi.py        # ASGI configuration
│   └── wsgi.py        # WSGI configuration
│
├── base/               # Main application
│   ├── templates/     # HTML templates
│   ├── models.py      # Database models
│   ├── views.py       # View functions
│   ├── urls.py        # App URL configuration
│   └── admin.py       # Admin interface configuration
│
└── manage.py          # Django management script
```

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd auth
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Features

- User authentication system
- User registration
- Login/Logout functionality
- Base templates for extending

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request
