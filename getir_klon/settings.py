from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-test-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin', # <--- EN ÜSTTE BU OLMALI
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # <--- Bizim uygulamamız
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

ROOT_URLCONF = 'getir_klon.urls'

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

WSGI_APPLICATION = 'getir_klon.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'tr' # Türkçe yaptık
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

# --- PANEL AYARLARI ---
JAZZMIN_SETTINGS = {
    "site_title": "İstegelsin Admin",
    "site_header": "İstegelsin",
    "site_brand": "İstegelsin",
    "welcome_sign": "Yönetici Paneline Hoşgeldiniz",
    "search_model": "core.Restoran",
    "topmenu_links": [{"name": "Siteyi Gör", "url": "/", "new_window": True}],
    "show_ui_builder": True,
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "brand_colour": "navbar-danger",
    "sidebar": "sidebar-dark-danger",
}
