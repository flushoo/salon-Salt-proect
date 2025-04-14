from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем ключи Stripe из переменных окружения
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-w5+ur_h=b%(=dk7su+f5edo&$10disq*)wdmt$1y9ani&hpwy*")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Подключенные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'booking',  # Приложение для барбершопа
    'django_bootstrap5',  # Bootstrap 5
]

# Middleware (Промежуточное ПО)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF защита
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основные настройки Django
ROOT_URLCONF = 'barbershop.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'booking' / 'templates'],  # Папка с шаблонами
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

# Настройки WSGI
WSGI_APPLICATION = 'barbershop.wsgi.application'

# База данных (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локализация и часовой пояс
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# 🔹 Настройки статических файлов (CSS, JS, изображения)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "booking" / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для сбора статики

# 🔹 Настройки медиа-файлов (загружаемые изображения)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Сессии
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Для хранения сессий в базе данных
SESSION_COOKIE_AGE = 3600  # Время жизни сессии в секундах (по умолчанию 3600 секунд = 1 час)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Удалять сессию, когда пользователь закрывает браузер

# CSRF защита
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG  # Включить только в production
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.com',
    'https://www.your-domain.com',
]

# Установка ключа для аутентификации
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔹 WhiteNoise — только в продакшене!
if not DEBUG:
    INSTALLED_APPS.insert(4, 'whitenoise.runserver_nostatic')  # Только если DEBUG=False
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Максимальный размер загружаемых файлов (100MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600

# Безопасность
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Подключение к Sentry (если нужно)
# SENTRY_DSN = os.getenv('SENTRY_DSN', '')







