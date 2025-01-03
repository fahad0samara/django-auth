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
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

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
