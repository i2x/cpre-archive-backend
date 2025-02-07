import os
from pathlib import Path
from datetime import timedelta

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: Load the secret key from environment variables or fallback (DO NOT use hardcoded keys in production)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-!+l6j76vk^$8b!apbm#7gkb1%*$p+lhwd=@2c2^8+_)3gsk&9n")

# SECURITY WARNING: Do not run with debug turned on in production
DEBUG = os.getenv("DEBUG", "True") == "True"

# Allowed hosts for production (Modify as needed)
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'taggit',  # Tagging system

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'social_django',

    # Custom apps
    'api',  # User management app
]

# Middleware (CORS Middleware MUST be first)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ Must be first for proper CORS handling
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT Authentication settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365 * 10),  # 10 years
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365 * 50),  # 50 years
    "ROTATE_REFRESH_TOKENS": False,  # No automatic refresh
    "BLACKLIST_AFTER_ROTATION": False,  # No blacklisting
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# 🔥 CORS CONFIGURATION 🔥
CORS_ALLOW_ALL_ORIGINS = True  # ✅ Allow all origins (for debugging; restrict in production)
CORS_ALLOW_CREDENTIALS = True  # ✅ Allow credentials for authentication

# If you want to restrict CORS to only certain frontend domains:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend (if using React)
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite frontend (if using Vue.js or React with Vite)
    "http://127.0.0.1:5173",
]

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'accept',
    'origin',
    'x-csrftoken',
    'x-requested-with',
]

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Google OAuth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# URL configuration
ROOT_URLCONF = 'backend.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'backend.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for development
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'api.CustomUser'
