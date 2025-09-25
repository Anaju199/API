from .common import *

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = {}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True # deixe False em localhost (True só em HTTPS)
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_HTTPONLY = False

CSRF_COOKIE_SAMESITE = "None" # para cross-site em produção pode ser 'None' (requer Secure=True)
