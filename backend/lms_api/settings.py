import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-only-change-this-secret')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '*').split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'corsheaders','rest_framework','rest_framework_simplejwt','lms_api.core',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware','django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'lms_api.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'lms_api.wsgi.application'

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    import urllib.parse
    p = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql','NAME':p.path.lstrip('/'),'USER':p.username,'PASSWORD':p.password,'HOST':p.hostname,'PORT':p.port or 5432,'OPTIONS': {'sslmode':'require'}}}
else:
    DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE='en-us'; TIME_ZONE='Asia/Dhaka'; USE_I18N=True; USE_TZ=True
STATIC_URL='/static/'; STATIC_ROOT=BASE_DIR/'staticfiles'; DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
CORS_ALLOWED_ORIGINS=[x.strip() for x in os.getenv('CORS_ALLOWED_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(',') if x.strip()]
CORS_ALLOW_CREDENTIALS=True
REST_FRAMEWORK={'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework_simplejwt.authentication.JWTAuthentication',),'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',)}
SIMPLE_JWT={'ACCESS_TOKEN_LIFETIME':timedelta(minutes=45),'REFRESH_TOKEN_LIFETIME':timedelta(days=7),'AUTH_HEADER_TYPES':('Bearer',)}
STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
