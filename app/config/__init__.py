from .celery import app as celery_app

# Django가 시작될 때 import가 진행되는 __init__.py
# shared_task가 장고에서 작동하도록 가능하게 해준다.
__all__ = ['celery_app']