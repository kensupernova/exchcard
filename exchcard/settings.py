# Django settings
#coding:utf-8
import os

ADMINS = (
    # ('admin', 'kenzhang1988@hotmail.com'),
)

# ##
# # ref: https://docs.djangoproject.com/en/dev/ref/settings/#email
# EMAIL_BACKEND = 'sae.ext.django.mail.backend.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'sender@gmail.com'
# EMAIL_HOST_PASSWORD = 'password'
# EMAIL_USE_TLS = True
# SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#
# MANAGERS = ADMINS

# Hosts/domain names that are valid for this exchard; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

## You must set settings.ALLOWED_HOSTS if DEBUG is False.
DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
USE_TZ = True
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-CN'

## set unicode
DEFAULT_CHARSET = "utf-8"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
# After continuing to search for django and pytz, I found the 1.6 Django release
#  notes, which mention that you must now install pytz to work with Sqlite3 if 
#  USE_TZ=True in your settings.py.
#I don't know what effect USE_TZ has on your application, but setting that value
# to False allows me to proceed in the tutorial. I would hope that the Django 
#tutorial is updated to reflect this change.



#### --------- 上传到服务器，127.0.0.1:8000+MEDIA_ROOT+'upload_to中的path'+图片名称
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          'media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
# STATIC_ROOT = ''

## The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting
# static_root is used for python manage.py collectstatic

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
## tuple with out comma,
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n#x%j+e4o2$g957%w-*rcut%4yp6w&*zb^w!+$*d&4_2bcaqh@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'exchcard.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'exchcard.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # django rest framework
    'rest_framework',
    'exchcard',
    'exchcard_backend_api',
    'oneverse',
    'oneverse_api',
)


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # admin user is the default permission for security
    # the permission of each view will be defined one by one specifically
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'PAGE_SIZE': 10
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the exchard admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
### UPLOAD HANDLERS
FILE_UPLOAD_HANDLERS=[
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
     "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

## login_required, 默认login地址
LOGIN_URL = "/account/login/"


### 配置SAE 新浪云
# 修改上传时文件在内存中可以存放的最大size为10m
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# sae的本地文件系统是只读的，修改django的file storage backend为Storage
## this one overide the MEDIA_ROOT
DEFAULT_FILE_STORAGE = 'sae.ext.django.storage.backend.Storage'
# 使用media这个bucket
STORAGE_BUCKET_NAME = 'exchcard_backend_api-bucket'
# ref: https://docs.djangoproject.com/en/dev/topics/files/

# 如何syncdb到线上数据库
# 在本地开发环境中，如下配置数据库，即可执行 python manage.py syncdb 直接syncdb到线上数据库。

## 用于本地调试
# from sae._restful_mysql import monkey
# monkey.patch()

## 线上数据库的配置
# MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
# MYSQL_PORT = '3307'
# MYSQL_USER = 'yn4j01zlxx'
# MYSQL_PASS = 'xl4w353h2h3h1315jzl2imx1hj0likwj1z2m125m'
# MYSQL_DB   = 'app_exchcard'
#
# # database setting for SAE My Sql
# DATABASES = {
#     'default': {
#         'ENGINE':   'django.db.backends.mysql',
#         'NAME':     MYSQL_DB,
#         'USER':     MYSQL_USER,
#         'PASSWORD': MYSQL_PASS,
#         'HOST':     MYSQL_HOST,
#         'PORT':     MYSQL_PORT,
#     }
# }


DATABASES = {
    'default': {
        # ## ---------------
        # use mysql database
        'ENGINE':'django.db.backends.mysql',
        'NAME':'exchcard',
        'USER':'zgh',
        'PASSWORD':'zgh123456',
        'HOST':'',
        'PORT':'',
    }
}