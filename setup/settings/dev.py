from .common import *

ALLOWED_HOSTS = ['*','127.0.0.1','localhost','10.0']
DEBUG = True
SECRET_KEY = "django-insecure-u+2-)=zkma-vjz$xn#p)4$#&b-)u&g86k$7@+mo%uo1c5)llde"

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_HTTPONLY = False

CSRF_COOKIE_SAMESITE = "Lax" # para cross-site em produção pode ser 'None' (requer Secure=True)