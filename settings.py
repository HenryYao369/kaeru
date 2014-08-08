import os, sys, socket

######################### Custom Kaeru Settings ##############################

ISPRODUCTION=(not (sys.argv[0] == "manage.py" or sys.argv[0] == "./manage.py"))
if ISPRODUCTION:
    TOPDIR = "/var/www/kaeru-lang.org/"
else:
    TOPDIR = os.getcwd()

if ISPRODUCTION:
    SITE_NAME = 'http://kaeru-lang.org'
else:
    SITE_NAME = 'http://127.0.0.1:8000'

# #key and certificate locations
# MASTER_CERTIFICATE_LOCATION = TOPDIR +"/keys/MasterCertificate.pem"
# CA_CERTIFICATE_LOCATION = TOPDIR +"/keys/CACertificate.pem"
# CA_KEY_LOCATION = TOPDIR +"/keys/KeyPair.pem"

# SESSION_COOKIE_DOMAIN="virtual-notary.org"
# PAYPAL_RECEIVER_EMAIL = "root@virtual-notary.org"

# EMAIL_HOST = 'cs.cornell.edu'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 25
# EMAIL_USE_TLS = True

# WEATHER_CHANNEL = 'yahoo'
# TWITTER_CONSUMER_KEY=''
# TWITTER_CONSUMER_SECRET=''
# TWITTER_ACCESS_KEY=''
# TWITTER_ACCESS_SECRET=''
# BITCOIN_SEND_ADDRESS = ''
# BITCOIN_RECEIVE_ADDRESS = ''
# BITCOIN_RECEIVE_ADDRESS = ''
# BITCOIN_TRANSACTION_AMOUNT = 0.0001
# TWITTER_URL = 'https://twitter.com/VNotary'

CORNELL_URL = 'http://www.cornell.edu/'
COMPUTER_SCIENCE_DEPARTMENT_URL = 'http://www.cs.cornell.edu/'

#RECAPTCHA
# RECAPTCHA_THRESHOLD_TIMEOUT = 60 * 60 # in seconds
# RECAPTCHA_THRESHOLD = 1000 # if increased to more than 10 increase DB field size to hold TimeStamp 
# RECAPTCHA_REQUIRED = False
# RECAPTCHA_PRIVATE_KEY = ''
# RECAPTCHA_PUBLIC_KEY = ''


######################## Django Settings #####################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Ross', 'ross@cs.cornell.edu'),
    ('Fabian', 'fabianm@cs.cornell.edu'),
    ('Ben', 'blg59@cornell.edu'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.sqlite3', # Options: 'postgresql_psycopg2', 'sqlite3', 'mysql', 'oracle'
        'NAME'    : '%s/%s' % (TOPDIR, 'db.db'),            # Path to database file, if using sqlite3
        # The following not used with sqlite3
        'USER'    : '',
        'PASSWORD': '',
        'HOST'    : '',
        'PORT'    : '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If false, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$-o#nstt9reaw9wwq*)i6d(t+qxl^k+5e3bb9pnrw)p)fs!)!#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Manage sessions across requests
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Associate user requests with sessions
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

# WGSI application used by Django's runserver.
WSGI_APPLICATION = 'kaeru.wsgi.application'

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/www/kaeru-lang.org/kaeru/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth', # Authentication framework
    'django.contrib.contenttypes', # Content type system, sets permissions on models
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'kaeru',
)

LOGIN_URL = "/login/"
