"""
Django settings for python_lms project.

Generated by 'django-admin startproject' using Django 4.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config, Csv
import os
import dj_database_url


OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_URL = config("OPENAI_URL")
GROQ_API_KEY = config("GROQ_API_KEY")
GROQ_MODEL = config("GROQ_MODEL")
GROQ_API_URL = config("GROQ_API_URL")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9od=10bdau&+gx5n4khdggg310w_5k^^=1v*2je0pytyd0v2+j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['.127.0.0.1','.localhost', '*','https://elikilms.up.railway.app/','elicode-021410ce9c03.herokuapp.com','www.kirateq.co.ke','kirateq.co.ke', '0.0.0.0', "https://90a1-102-0-21-4.ngrok-free.app"]
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'learning',
    'verify_email.apps.VerifyEmailConfig',
    'django_ckeditor_5',
   
]

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload','CodeBlock','Table',
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'Undo', 'Redo']},
            {'name': 'alignment', 'items': ['alignment:left', 'alignment:center', 'alignment:right', 'alignment:justify']},
            {'name': 'editing', 'items': ['Find', 'Replace', 'SelectAll']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', 'Blockquote', 'CreateDiv']},
            {'name': 'insert', 'items': ['ImageUpload', 'Table', 'HorizontalRule', 'SpecialChar']},  # Add CodeBlock
            {'name': 'styles', 'items': ['Styles', 'Format']},
            {'name': 'tools', 'items': ['Maximize']}, 
            ],
         'image': {
            'toolbar': [
                'imageTextAlternative', 
                'imageTitle', 
                '|', 
                'imageStyle:alignLeft', 
                'imageStyle:full', 
                'imageStyle:alignRight', 
                'imageStyle:alignCenter', 
                'imageStyle:side'
            ],
            'styles': ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter']
        },
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote', 'imageUpload'
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],

        'image': {
            'toolbar': ['imageTextAlternative', 'imageTitle', '|', 'imageStyle:alignLeft', 'imageStyle:full',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',]
            },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                
            },
            'tableCellProperties': {
                
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ],
             'height': 400,
        'width': '100%',
        'image': {'upload': {'url': '/ckeditor5/upload/'}},
        'filebrowserUploadUrl': '/ckeditor5/upload/',
        'extraPlugins': ['image2', 'uploadimage', 'autolink', 'codeBlock'],  # Include the CodeBlock plugin
        }
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.staticfiles.middleware.StaticFilesMiddleware',
]

ROOT_URLCONF = 'python_lms.urls'

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

WSGI_APPLICATION = 'python_lms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if config('MODE')=='dev':
     DATABASES = {
    

        #    'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / 'db.sqlite3',  # This stores the SQLite3 database in the project root
    # }
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DB_NAME'),
            'USER':config('DB_USER'),
            'PASSWORD':config("DB_PASSWORD"),
            'HOST':config('DB_HOST'),
            'PORT':config('DB_PORT')
            
        }
    
     }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default= config('DATABASE_URL')
        )
         

    
    }


    # DATABASES = {
    

    #        'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': BASE_DIR / 'db.sqlite3',  # This stores the SQLite3 database in the project root
    # }
    


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)





# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast= Csv())
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL ='/login/'
LOGIN_REDIRECT_URL = '/'
# AUTH_USER_MODEL ='learning.CustomUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATIC_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email credentials
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


ADMIN_USER_NAME=config("ADMIN_USER_NAME", default="Admin user")
ADMIN_USER_EMAIL=config("ADMIN_USER_EMAIL", default=None)

MANAGERS=[]
ADMINS=[]
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS +=[
        (f'{ADMIN_USER_NAME}', f'{ADMIN_USER_EMAIL}')
    ]
    MANAGERS=ADMINS

