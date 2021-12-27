"""
Django settings for ktm project project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
# fist import the needed packages
import ldap
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap.config import ActiveDirectoryGroupType


from pathlib import Path
import environ
env = environ.Env()
environ.Env.read_env()



#import library to logging configuration : 
import os
import logging.config
import logging # must be imported in view.py also.
from django.utils.log import DEFAULT_LOGGING

# Internationalization

from django.utils.translation import gettext, ngettext
from django.utils.translation import gettext_lazy as _

# messages :
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8g-804gv!!s53=a7ahuz#u7pef3#jx@7(r!h1&av=*8f%)a91#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [env('APP_SERVER'),'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # configure the accounts app 
    'accounts.apps.AccountsConfig',
    #'rosetta',  # Rosetta Translation Interface
    'parler', #Translating Models with django-parler
    # Custom for contact application
    #'contact',
    # 3rd party apps
    'crispy_forms',
    'TaskManagement.apps.TaskManagementConfig',
     # configure the MeetingRoom app 
    'MeetingRoom.apps.MeetingRoomConfig',
    'bootstrap_datepicker_plus',
    #'flatpickr',
    'bootstrap4',
    
]

# Indicates the frontend framework django crispy forms use
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware', # For localization and translation settings
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'KTM_Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
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

#WSGI_APPLICATION = 'ktm_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT':env( 'DB_PORT'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

#LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Here specified the languages we want our project to be available in
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('ar', _('Arabic')),
)


PARLER_LANGUAGES = {
    None: (
        {'code': 'en',}, # English
        {'code': 'fr',}, # French
        {'code': 'ar',}, # Arabic
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}

# locale path directory for your application where message files will reside

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



'''
# LDAP CONFIGRATION START HERE !


AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = "CN=bind,CN=Users,DC=BD,DC=COM"
AUTH_LDAP_BIND_PASSWORD = env('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=BD,dc=COM", ldap.SCOPE_SUBTREE, "sAMAccountName=%(user)s")
AD_SEARCH_FIELDS= ['mail','givenName','sn','sAMAccountName','memberOf']

AUTH_LDAP_USER_ATTR_MAP = {
"username": "sAMAccountName",
"first_name": "givenName",
"last_name": "sn",
"email": "mail",
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("dc=BD,dc=COM", ldap.SCOPE_SUBTREE, "(objectCategory=Group)")

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {"is_superuser": "CN=django-admin,CN=Users,DC=BD,DC=COM","is_staff": "CN=django-admin,CN=Users,DC=BD,DC=COM",}

AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1  # 1 hour cache

AUTHENTICATION_BACKENDS = [
'django_auth_ldap.backend.LDAPBackend',
'django.contrib.auth.backends.ModelBackend',

]
# TO INCREASE THE SPEED 

AUTH_LDAP_CONNECTION_OPTIONS = {
ldap.OPT_DEBUG_LEVEL: 0,
ldap.OPT_REFERRALS: 0,
}


# LDAP CONFIGRATION ENDS HERE !
'''
#Mail service



EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST =env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =env('EMAIL_HOST_PASSWORD')


#####################################################
# Configuring logging settings for StreamHandeler (Console):
# Disabling logging configuration below settings only when need to disable default django logging :
# LOGGING_CONFIG = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
   #"root": {"level": "DEBUG", "handlers": ["console"]},
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "test_format",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True
        },
    },
    "formatters": {
        "test_format": {
            "format": (
                u"[%(asctime)s] [%(levelname)-4s]  [%(name)-12s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S %p %Z %z",
        },
    }, 
}



ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "../../detail/%s/" % u.id,
}