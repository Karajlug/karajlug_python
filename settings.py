<<<<<<< local
Debugger entered--Lisp error: (void-function smart-operator-mode-on)
  (smart-operator-mode-on)
  (lambda nil (set-variable (quote py-indent-offset) 4) (set-variable (quote indent-tabs-mode) nil) (define-key py-mode-map (kbd "RET") (quote newline-and-indent)) (smart-operator-mode-on))()
  run-hooks(python-mode-hook)
  python-mode()
  funcall(python-mode)
  (progn (funcall mode) mode)
  (if mode (progn (funcall mode) mode))
  (when mode (funcall mode) mode)
  (if (and keep-mode-if-same (eq ... ...)) nil (when mode (funcall mode) mode))
  (unless (and keep-mode-if-same (eq ... ...)) (when mode (funcall mode) mode))
  mumamo-ad-set-auto-mode-0(python-mode nil)
  set-auto-mode-0(python-mode nil)
  set-auto-mode()
  normal-mode(t)
  after-find-file(nil t)
  find-file-noselect-1(#<buffer settings.py> "~/Project's/FSF/karajlug_org/settings.py" nil nil "~/Project's/FSF/karajlug_org/settings.py" (11821111 2051))
  find-file-noselect("~/Project's/FSF/karajlug_org/settings.py" nil nil t)
  find-file("~/Project's/FSF/karajlug_org/settings.py" t)
  call-interactively(find-file nil nil)
=======
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.devdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ROOT = os.path.dirname(__file__)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tehran'

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
MEDIA_ROOT = os.path.join(ROOT, 'statics').replace("\\", "/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/statics/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'gjf)nm7ksjh@*vaiax%2u)tnlig4$yq5fm-99tszdx=75f4ak1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates').replace("\\", "/")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    "news",
    "faq",
)

NEWS_LIMIT = 10
>>>>>>> other
