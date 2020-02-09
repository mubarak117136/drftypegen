from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['']
SESSION_COOKIE_SECURE = True

HTML_MINIFY = True
MIDDLEWARE = MIDDLEWARE + ['htmlmin.middleware.HtmlMinifyMiddleware',
                            'htmlmin.middleware.MarkRequestMiddleware']
