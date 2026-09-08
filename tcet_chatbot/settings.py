"""
Django settings for the TCET Chatbot project.

This is a SMALL COLLEGE PROJECT, so the settings are kept as simple
as possible (no environment variable managers, no cloud config, etc).
"""

from pathlib import Path

# BASE_DIR points to the folder that contains manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------
# SECURITY (kept simple on purpose - this is NOT a production app)
# -----------------------------------------------------------------
SECRET_KEY = 'django-insecure-tcet-chatbot-college-project-key'

DEBUG = True  # Shows helpful error pages while developing

ALLOWED_HOSTS = ['*']  # Fine for a local college project/demo

# -----------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chatbot',  # our app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tcet_chatbot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django will look inside chatbot/templates/ automatically
        # because APP_DIRS is True. DIRS is left empty on purpose.
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

WSGI_APPLICATION = 'tcet_chatbot.wsgi.application'

# -----------------------------------------------------------------
# DATABASE - SQLite (a single file, no server setup needed)
# -----------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------------------------------
# PASSWORD VALIDATION (Django defaults - only affects admin login)
# -----------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------
# STATIC FILES (CSS, JS)
# -----------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
