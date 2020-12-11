from .settings import *
import os

DEBUG = False

hostname = os.environ['DBHOST']

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']
                 ] if 'WEBSITE_HOSTNAME' in os.environ else []

# Configure Postgres database; the full username is username@servername,
# which we construct using the DBHOST value.

my_mane_is = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'] + "@" + hostname,
        'PASSWORD': os.environ['DBPASS']
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}
DEFAULT_FILE_STORAGE = 'animeSite.custom_azure.AzureMediaStorage'
STATICFILES_STORAGE = 'animeSite.custom_azure.AzureStaticStorage'

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

AZURE_ACCOUNT_NAME = "djangoforumstorage"
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
CKEDITOR_BASEPATH = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/ckeditor/ckeditor/'
