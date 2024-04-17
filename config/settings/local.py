from .base import *

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_USE_TLS = False
