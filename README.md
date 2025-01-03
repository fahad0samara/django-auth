<<<<<<< HEAD
# CRM System with Two-Factor Authentication

A Django-based Customer Relationship Management (CRM) system with enhanced security features including two-factor authentication.

## Features

- User Authentication with Email
- Two-Factor Authentication (2FA)
- Social Authentication (Google, GitHub)
- Customer Management
- Secure Password Reset
- Modern, Responsive UI

## Project Structure

```
auth/
├── auth/                   # Project configuration
│   ├── settings.py         # Project settings
│   └── urls.py            # Main URL configuration
├── crm/                    # CRM application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # CRM URLs
│   └── templates/         # CRM templates
├── templates/             # Global templates
│   ├── account/          # Authentication templates
│   ├── two_factor/       # 2FA templates
│   ├── base.html         # Base template
│   └── home.html         # Homepage template
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
=======
# Django Authentication Project

This Django project provides a simple authentication system allowing users to sign up and log in. It includes a homepage accessible only to logged-in users.

## Features

- **User Authentication**: Users can sign up for an account and log in securely.
- **Homepage**: Logged-in users are redirected to the homepage upon successful authentication.
- **Built-in Forms**: Utilizes Django's built-in forms for user authentication and user creation.

## Installation

1. Clone the repository:



2. Install dependencies:

>>>>>>> 27477ccc6e2b5d95c50d9db23c16a7c580df1496
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
<<<<<<< HEAD
=======

>>>>>>> 27477ccc6e2b5d95c50d9db23c16a7c580df1496
   ```bash
   python manage.py migrate
   ```

<<<<<<< HEAD
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
=======
4. Run the development server:

>>>>>>> 27477ccc6e2b5d95c50d9db23c16a7c580df1496
   ```bash
   python manage.py runserver
   ```

<<<<<<< HEAD
## Configuration

1. Email Settings (in settings.py):
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   ```

2. Social Authentication:
   - Configure Google OAuth in the Django admin
   - Configure GitHub OAuth in the Django admin

## Security Features

- Two-Factor Authentication using TOTP
- Secure password hashing
- CSRF protection
- Session security
- Email verification

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
=======
5. Access the application at `http://localhost:8000/`.

## Usage

- Visit the homepage to sign up for an account or log in if you already have one.
- After successful authentication, you will be redirected to the homepage.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.








>>>>>>> 27477ccc6e2b5d95c50d9db23c16a7c580df1496
