from .base import *

# Import Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = True

WSGI_APPLICATION = 'config.wsgi.application'

secrets = json.load(open(os.path.join(SECRETS_DIR, 'development.json')))

DATABASES = secrets['DATABASES']

ALLOWED_HOSTS = secrets['ALLOWED_HOST']

# Sentry settings
sentry_sdk.init(
    dsn=secrets["SENTRY_DSN"],
    integrations=[DjangoIntegration()]
)

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # 1번 DB
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# MultiDB Router for OPEN API(information applicatoin)
DATABASE_ROUTERS = [
    'information.routers.OpenAPIDBRouter'
]