"""
Django settings for animeSite project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e4io4-+#wc3sb=h)#y@y3cg^^ao6#@44cy*y0p2*s^a94-n9gm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_pagination',
    'forum',
    'member.apps.MemberConfig',
    'ckeditor',
    'ckeditor_uploader',
    'multiselectfield',
    'django_cleanup',
    'autoslug',
    'easy_thumbnails',
    'storages'
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

ROOT_URLCONF = 'animeSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'animeSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

CKEDITOR_UPLOAD_PATH = 'uploads/'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'

CKEDITOR_CONFIGS = {
    'default': {
        'uiColor': '#ADD8E6',
        'toolbar': 'custom',
        'width': '100%',
        'toolbar': [["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker"],
                    ['TextColor', 'BGColor'],
                    ['Styles', 'FontSize'],
                    ['NumberedList', 'BulletedList', 'JustifyLeft', 'JustifyCenter',
                     'JustifyRight', 'JustifyBlock'],
                    ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink",
                        "Subscript", "Superscript", "Smiley"],
                    ['Undo', 'Redo'],
                    ["Maximize", "Preview"], ],


    },
    'reply_box': {
        'uiColor': '#ADD8E6',
        'toolbar': 'custom',
        'height': '200%',
        'width': '100%',
        'toolbar': [["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker"],
                    ['NumberedList', 'BulletedList', 'JustifyLeft', 'JustifyCenter',
                     'JustifyRight', 'JustifyBlock'],
                    ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink",
                        "Subscript", "Superscript"], ['Undo', 'Redo'],
                    ["Maximize"]],
        'extraPlugins': ','.join(
            [
                # you extra plugins here
                'autocomplete',
                'mentions',
                'textmatch',
                'textwatcher',
            ]),
        'mentions': [{'feed': '/search/?query={encodedQuery}', 'minChars': 0,
                      'itemTemplate': '<li data-id="{id}"><img src="{iconSrc}" alt="{name}" width=32 height=32 class=mr-1>{name}</li>',
                      'outputTemplate': "<a href={userSrc}>{name}</a>"
                      }],
    },
}

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
