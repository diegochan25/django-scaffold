from pathlib import Path
from environ import Env


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = Env()

Env.read_env(BASE_DIR / '.env')

PYTHON_ENV = env.str('PYTHON_ENV', default='development', choices=['development', 'testing', 'staging', 'production'])

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
SECRET_KEY = env.str('SECRET_KEY')

DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DB_NAME = env.str('DB_NAME')

S3_ENDPOINT = env.str('S3_ENDPOINT')
S3_REGION = env.str('S3_REGION', default='us-east-1')
S3_ACCESS_KEY = env.str('S3_ACCESS_KEY')
S3_SECRET_KEY = env.str('S3_SECRET_KEY')
S3_BUCKET = env.str('S3_BUCKET')

SMTP_USER = env.str('SMTP_USER')
SMTP_PASSWORD = env.str('SMTP_PASSWORD')
SMTP_HOST = env.int('SMTP_HOST')
SMTP_PORT = env.str('SMTP_PORT')
SMTP_STARTTLS = env.str('SMTP_STARTTLS')
SMTP_FROM = env.str('SMTP_FROM')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'procrastinate.contrib.django',
    'django_vite',
    'apps.accounts',
    'apps.core'
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

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'accounts.User'

SERIALIZATION_MODULES = {
    'yml': 'django.core.serializers.pyyaml',
}

CONTEXT_PROCESSORS = [
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS
        }
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'jinja2'],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'config.jinja2.environment',
            'context_processors': CONTEXT_PROCESSORS
        }
    }
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'NAME': DB_NAME,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' }
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_ROOT = 'public/'

DJANGO_VITE = {
    'default': {
        'dev_mode': env.bool('VITE_DEV_MODE', default=PYTHON_ENV == 'development'),
        'static_url_prefix': 'vite',
        'manifest_path': BASE_DIR / 'static' / 'vite' / '.vite' / 'manifest.json',
        'dev_server_host': 'localhost',
        'dev_server_port': 5173,
    }
}

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'endpoint_url': S3_ENDPOINT,
            'access_key': S3_ACCESS_KEY,
            'secret_key': S3_SECRET_KEY,
            'region_name': S3_REGION,
            'bucket_name': S3_BUCKET
        }
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    }
}

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'username': SMTP_USER,
            'password': SMTP_PASSWORD,
            'host': SMTP_HOST,
            'port': SMTP_PORT,
            'use_tls': SMTP_STARTTLS
        }
    }
}
