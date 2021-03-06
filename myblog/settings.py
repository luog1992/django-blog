# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't+28ustkn(oknld!h_9t9e%&4l*g36^pl+(es&93dr0blb6u4p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# celery settings
import djcelery
djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
# celery periodic task: get_celery_result
CELERYBEAT_SCHEDULE = {
    'get_celery_result': {
        # the func will be executed at the tasks module
        'task': 'article.tasks.get_celery_result',
        'schedule': datetime.timedelta(seconds=10),
    }
}

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django_summernote',
    # celery related app
    'djcelery',
    'kombu.transport.django',
    # duoshuo comments
    'duoshuo',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'article',
)

# DuoSHuo Settings
DUOSHUO_SECRET = 'e041c01fb314345b3776e232487cfe51'
DUOSHUO_SHORT_NAME = 'xianyuu'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'myblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR + '/templates',],
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/article'),
        ],
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

WSGI_APPLICATION = 'myblog.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj_myblog',
        'USER': 'root',
        'PASSWORD': 123456,
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LOGIN_URL = '/login/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '100%',
    'height': '1000',

    # Use proper language setting automatically (default)
    'lang': None,

    # Customize toolbar buttons
    # 'toolbarContainer': '.my-toolbar',
    'toolbar': [
        ['style', ['style']],
        ['color', ['color']],
        ['fontstyle', ['bold', 'clear']],
        ['fontsize', ['fontname', 'fontsize']],
        ['para', ['ul', 'ol', 'paragraph', 'height']],
        ['insert', ['link', 'hr', 'picture', 'table']],
        ['Misc', ['undo', 'redo']],
    ],

    # You can add custom css/js for SummernoteWidget.
    # 'css': (
    #     os.path.join(BASE_DIR, "article/static/summernote_custom.css"),
    # ),

}
