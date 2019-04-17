"""
Django settings for oursite project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import pymysql


pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^rrh0xz8+1y3-o48s0vp*q0!2_c(s%so#!^ldmmlef0qftxbty'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

AUTH_USER_MODEL = 'auth.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
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



ROOT_URLCONF = 'oursite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'oursite.wsgi.application'

FILE_UPLOAD_MAX_MEMORY_SIZE = 429916160
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#MySQL 연동 설정

DATABASES = {
    'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'main_project', # DB명
          'USER': 'root', # 데이터베이스 계정
          'PASSWORD': 'kor099060', # 계정 비밀번호
          'HOST': '127.0.0.1', # 데이테베이스 주소(IP)
          'PORT': '3306', # 데이터베이스 포트(보통은 3306)
      }
}




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/main/mypage/'  #로그인시 리다이렉트 경로설정
LOGOUT_REDIRECT_URL = '/main/login/'  #로그아웃시 리다이렉트 경로설정
SIGNUP_REDIRECT_URL = '/main/mypage/'  #회원가입 완료시 리다이렉트 경로설정

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul' #한국 시간으로 설정

USE_I18N = True

USE_L10N = True

USE_TZ = True

#css, javascript, images 파일과 같은 정적파일을 보관하는 경로
STATIC_URL = '/static/'

# 앱별로 static 폴더 관리하게 해주는 옵션이라고 함.(없어도 되는데 뭔지 확인해봐야함)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# 각 media 파일에 대한 URL Prefix
MEDIA_URL = '/documents/' # 항상 / 로 끝나도록 설정
# MEDIA_URL = 'http://static.myservice.com/media/' 다른 서버로 media 파일 복사시

# 업로드된 파일을 저장할 디렉토리 경로
MEDIA_ROOT = os.path.join(BASE_DIR, 'documents')
