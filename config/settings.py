import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = bool(int(os.environ.get('DEBUG', 1)))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    'debug_toolbar',
    'django_filters',
    'ckeditor',

    'api.v1.general.apps.GeneralConfig',
    'api.v1.accounts.apps.AccountsConfig',
    'api.v1.authentications.apps.AuthenticationsConfig',
    'api.v1.payments.apps.PaymentsConfig',
    'api.v1.discounts.apps.DiscountsConfig',
    'api.v1.tariffs.apps.TariffsConfig',
    'api.v1.chapters.apps.ChaptersConfig',
    'api.v1.lessons.apps.LessonsConfig',
    'api.v1.questions.apps.QuestionsConfig',
    'api.v1.exams.apps.ExamsConfig',
    'api.v1.swish.apps.SwishConfig'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'api.v1.general.middleware.LanguageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': os.environ.get('DB_HOST'),
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASS'),
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379',
        'OPTIONS': {
            'db': 1
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
LOGIN_REDIRECT_URL = '/api/v1/accounts/profile'

# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TOKEN_EXPIRE_DAY = 7

FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
GOOGLE_CLIENT_ID_ANDROID = os.environ.get('GOOGLE_CLIENT_ID_ANDROID')
GOOGLE_CLIENT_ID_IOS = os.environ.get('GOOGLE_CLIENT_ID_IOS')
GOOGLE_CLIENT_ID_WEB = os.environ.get('GOOGLE_CLIENT_ID_WEB')
SOCIAL_SIGN_IN_IDS = [GOOGLE_CLIENT_ID_ANDROID, GOOGLE_CLIENT_ID_IOS, GOOGLE_CLIENT_ID_WEB]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.v1.authentications.authentication.CustomTokenAuthentication'
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'api.v1.accounts.permissions.IsStudent'
    ],
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',

    'DEFAULT_PAGINATION_CLASS': None,
    'PAGE_SIZE': None,

    'DEFAULT_FILTER_BACKENDS': [],

    'DATE_FORMAT': '%Y-%m-%d',
    'DATE_INPUT_FORMATS': ['%Y-%m-%d'],

    'DATETIME_FORMAT': '%Y-%m-%d %H:%M',
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M'],

    'TIME_FORMAT': '%H:%M',
    'TIME_INPUT_FORMATS': ['%H:%M'],
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ['rest_framework.authentication.BasicAuthentication',
                                                         'rest_framework.authentication.SessionAuthentication']

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_TRACK_STARTED = True  # last
CELERY_TASK_TIME_LIMIT = 30 * 60  # last

CORS_ALLOW_ALL_ORIGINS = True

# stripe
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY_TEST')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY_TEST')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
STRIPE_CHECKOUT_TIMEOUT = 30 * 60  # in second
STRIPE_CHECKOUT_CURRENCY = 'SEK'

FRONT_DOMAIN = os.environ.get('FRONT_DOMAIN', f'https://{ALLOWED_HOSTS[0]}')  # frontend domain  # last

WEB_FORGOT_PASSWORD_URL = '/api/v1/auth/password-reset/confirm/link/?uid={}&token={}'  # last
WEB_FORGOT_PASSWORD_URL = FRONT_DOMAIN + WEB_FORGOT_PASSWORD_URL

SUCCESS_PAYMENT_URL = 'https://google.com'
FAILURE_PAYMENT_URL = 'https://youtube.com'

TEST_BALL = 1
LESSON_BALL = 10
MAX_QUESTIONS = 65
MAX_WRONG_QUESTIONS = 20
MIN_QUESTIONS = 5
CUSTOM_LANGUAGES = ['swe', 'en', 'e_swe']
LEVEL_CORRECT_COUNTS = [0, 50, 150, 300, 500, 750, 1150, 1650, 2350, 3200]
LEVEL_NAMES = {
    'en': [
        'Nyckelknippe',
        'Startmotorn',
        'Asfaltsrookie',
        'Kopplingskung',
        'Vägkapten',
        'Kurvmästare',
        'Gasguru',
        'Fartfantast',
        'Bilboss',
        'Körkortskung'
    ],
    'e_swe': [
        'Nyckelknippe',
        'Startmotorn',
        'Asfaltsrookie',
        'Kopplingskung',
        'Vägkapten',
        'Kurvmästare',
        'Gasguru',
        'Fartfantast',
        'Bilboss',
        'Körkortskung'
    ],
    'swe': [
        'Nyckelknippe',
        'Startmotorn',
        'Asfaltsrookie',
        'Kopplingskung',
        'Vägkapten',
        'Kurvmästare',
        'Gasguru',
        'Fartfantast',
        'Bilboss',
        'Körkortskung',
    ]
}

# smtp configs
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

AUTH_USER_MODEL = 'accounts.CustomUser'

INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
    '16.171.170.49'
]

if DEBUG:
    INTERNAL_IPS += ALLOWED_HOSTS

JAZZMIN_SETTINGS = {
    "site_header": 'test header',
    "site_brand": 'test brand',
    "site_logo": 'logos/site-logo.png',
    "copyright": 'test copyright',
}

# CKEDITOR_CONFIGS = {
#     'default': {
#         # 'skin': 'moono',
#         # 'skin': 'office2013',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
#             {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
#             {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
#             {'name': 'forms',
#              'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
#                        'HiddenField']},
#             '/',
#             {'name': 'basicstyles',
#              'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
#             {'name': 'paragraph',
#              'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
#                        'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
#                        'Language']},
#             {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#             {'name': 'insert',
#              'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
#             '/',
#             {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
#             {'name': 'colors', 'items': ['TextColor', 'BGColor']},
#             {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
#             {'name': 'about', 'items': ['About']},
#             '/',  # put this to force next toolbar on new line
#             {'name': 'yourcustomtools', 'items': [
#                 # put the name of your editor.ui.addButton here
#                 'Preview',
#                 'Maximize',
#                 'Youtube'
#             ]},
#         ],
#         'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
#         # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
#         # 'height': 291,
#         # 'width': '100%',
#         # 'filebrowserWindowHeight': 725,
#         # 'filebrowserWindowWidth': 940,
#         # 'toolbarCanCollapse': True,
#         # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
#         'tabSpaces': 4,
#         'extraPlugins': ','.join([
#             'uploadimage',  # the upload image feature
#             # your extra plugins here
#             'div',
#             'autolink',
#             'autoembed',
#             'embedsemantic',
#             'autogrow',
#             # 'devtools',
#             'widget',
#             'lineutils',
#             'clipboard',
#             'dialog',
#             'dialogui',
#             'elementspath',
#             'youtube'
#         ]),
#     }
# }
