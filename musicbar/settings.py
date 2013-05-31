# Django settings for squash project.

import logging
import settings_local

DEBUG = settings_local.DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Par Trivedi', 'par.triv@gmail.com'),
     ('Stephen Johnston', 'se.johnston@gmail.com')
)

MANAGERS = ADMINS

ALLOWED_HOSTS = '*'

DATABASES = {
    'default': {
                'ENGINE':'django.db.backends.mysql',
        
        'NAME': 'squashmusic',                      # Or path to database file if using sqlite3.
        'USER': settings_local.MYSQL_USER,                      # Not used with sqlite3.
        'PASSWORD': settings_local.MYSQL_PASSWORD,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
#

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Resolute'

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = settings_local.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = settings_local.MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'yf%*-v_jfuqwec;0o2pqhns07d6*xm82irjfmgih#dkb(p@6pl'

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
    'musicbar.exception.handler.middleware',
)

APPEND_SLASH = True
PREPEND_WWW = False

ROOT_URLCONF = 'musicbar.urls'

TEMPLATE_DIRS = settings_local.TEMPLATE_DIRS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'musicbar'
)


#-----------------------#
# LOGGING SETTINGS      #
#-----------------------#
if not hasattr(logging, "set_up_done"):
    logging.set_up_done=False

if not logging.set_up_done:
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logger = logging.getLogger()
    stdoutHandler = logging.StreamHandler()
    stdoutHandler.setLevel( logging.DEBUG )
    stdoutHandler.setFormatter( logging.Formatter( LOG_FORMAT ) )
    logger.setLevel(logging.DEBUG)
    logger.addHandler( stdoutHandler )
    
    if DEBUG:
        logging.getLogger('django.db.backends').setLevel(logging.ERROR)
        """
        logger = logging.getLogger('django.db')
        stdoutHandler = NullHandler()
        stdoutHandler.setLevel( logging.DEBUG )
        stdoutHandler.setFormatter( logging.Formatter( LOG_FORMAT ) )
        logger.setLevel(logging.DEBUG)
        logger.addHandler( stdoutHandler )
        """
    
    logging.set_up_done=True
    print "set up logging"    
    logger.info("set up logging")


SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 631138519
SESSION_COOKIE_NAME = 'musicbarsq_id'
