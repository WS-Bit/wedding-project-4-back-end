from pathlib import Path
import os
import environ
from dotenv import load_dotenv
import django_on_heroku
import dj_database_url

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Determine the environment
ENV = os.getenv('ENVIRONMENT', 'DEV')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-kjwpunl0@d45ablg)wu5fi&688xem^3=(mg@j&)o-x06rmulh)')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV == 'DEV'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'wedding-back-end-ga-32f0d464c773.herokuapp.com'] if ENV == 'DEV' else ['your-production-domain.com']

SITE_PASSWORD = os.getenv('SITE_PASSWORD')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'phonenumber_field',
    'guests',
    'rsvp',
    'songrequests',
    'memories',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "project.middleware.PasswordProtectionMiddleware"
]

# CORS and CSRF settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://wedding-front-end-ga.netlify.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://wedding-back-end-ga-32f0d464c773.herokuapp.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://wedding-front-end-ga.netlify.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://wedding-back-end-ga-32f0d464c773.herokuapp.com",
]

# Add these headers explicitly if not added already
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "accept-language",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# Ensure credentials are allowed for cookies (CSRF)
CSRF_COOKIE_SECURE = False  # Set to True when using HTTPS
CSRF_COOKIE_SAMESITE = 'None'  # Needed for cross-origin requests
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE = ENV == 'PROD'
SESSION_COOKIE_HTTPONLY = True

# Add your static files handling here

ROOT_URLCONF = 'project.urls'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Configure Django App for Heroku
django_on_heroku.settings(locals())

# Override DATABASE_URL after django_on_heroku setup
if ENV == 'DEV' and 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

SECURE_SSL_REDIRECT = ENV == 'PROD'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
