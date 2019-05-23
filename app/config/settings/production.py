from .base import *

# Import Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

WSGI_APPLICATION = 'config.wsgi.application'

secrets = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))

# .secrets의 production.json을 사용
# SECRET_KEY는 이미 base.py에서 base.json으로 import 했으므로,
# production.json에는 DATABASE : ec2_deploy 설정만 기록
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
        "LOCATION": "redis://localhost:6379/1",  # 1번 DB
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}