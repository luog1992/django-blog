from __future__ import absolute_import
from celery import shared_task
from celery import task
from celery.result import AsyncResult


@shared_task()
def add(x, y):
    return x + y


@shared_task()
def mul(x, y):
    return x * y

@shared_task()
def get_celery_result():
    id = '288a1819-c1b2-46d4-b0b4-3049436898e6'
    work = AsyncResult(id)
    if work.ready():
        try:
            result = work.get(timeout=1)
            return result
        except:
            pass
    return 'Please waiting for the result'

@task()
def test():
    return 'The celery admin works'
