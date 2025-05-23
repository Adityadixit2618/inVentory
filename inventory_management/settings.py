"""
Django settings for inventory_management project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-w07&5gwrdk==i^43uy8szu2ftmy_-izw!_-((jd!p-e5l)whj6')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = [
    'web-production-62941.up.railway.app',
    'inventory.com',
    'localhost',
    '127.0.0.1',
    '*',  # Temporarily allow all hosts
]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-62941.up.railway.app',
    'https://inventory.com',
    'http://localhost',
    'http://127.0.0.1',
]

# Security Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# Application definition

INSTALLED_APPS = [
    'inventory',
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'inventory_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# Database Configuration
print("Checking environment variables...")
print(f"DATABASE_URL present: {'DATABASE_URL' in os.environ}")
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    print(f"Found DATABASE_URL: {DATABASE_URL[:10]}...")  # Only print the beginning for security
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    print("WARNING: DATABASE_URL not found. Using SQLite for development.")
    print("Available environment variables:", list(os.environ.keys()))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Print database info for debugging
db_config = DATABASES['default']
print(f"Current Database Engine: {db_config['ENGINE']}")
print(f"Debug Mode: {DEBUG}")
print(f"Allowed Hosts: {ALLOWED_HOSTS}")

# Ensure we're using PostgreSQL in production
if not DEBUG and not DATABASE_URL:
    raise Exception(
        'DATABASE_URL environment variable is required when DEBUG=False'
    )

# Print database info for debugging (will show up in Railway logs)
if not DEBUG:
    db_config = DATABASES['default']
    print(f"Database Engine: {db_config['ENGINE']}")
    if 'sqlite' in db_config['ENGINE'].lower():
        print("WARNING: Using SQLite in production is not recommended!")


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Simplified static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Create static root if it doesn't exist
os.makedirs(STATIC_ROOT, exist_ok=True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = '/dashboard'
LOGIN_URL = 'login'

LOW_QUANTITY = 3

# Comment out the production security settings for now
# if not DEBUG:
#     # HTTPS settings
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
#     # HSTS settings
#     SECURE_HSTS_SECONDS = 31536000  # 1 year
#     SECURE_HSTS_PRELOAD = True
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Security Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Set to True in production
SESSION_COOKIE_SECURE = False  # Set to True in production
CSRF_COOKIE_SECURE = False  # Set to True in production

# Debug settings
DEBUG = True  # Temporarily set to True to see detailed error messages
