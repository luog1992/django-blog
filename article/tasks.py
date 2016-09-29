from __future__ import absolute_import
from celery import shared_task
from celery.result import AsyncResult


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def get_celery_result():
    id = '26bc7937-928f-4d00-8868-5ce568ae2713'
    work = AsyncResult(id)
    if work.ready():
        try:
            result = work.get(timeout=1)
            return result
        except:
            pass
    return 'Please waiting for the result'

