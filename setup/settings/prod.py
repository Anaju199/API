from .common import *

ALLOWED_HOSTS = ['*','127.0.0.1','localhost','10.0']
DEBUG = True
SECRET_KEY = "django-insecure-u+2-)=zkma-vjz$xn#p)4$#&b-)u&g86k$7@+mo%uo1c5)llde"

# Trust em HTTPS (se usa proxy/reverse proxy tipo Nginx ou Cloudflare)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies só via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Necessário se o frontend for separado do backend (cross-site requests)
CSRF_COOKIE_SAMESITE = "None"


SESSION_COOKIE_SAMESITE = "None"

# Se quiser que o JS consiga ler o cookie
CSRF_COOKIE_HTTPONLY = True
