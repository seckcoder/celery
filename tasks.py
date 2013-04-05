from celery import Celery
import celery_config

celery = Celery('tasks')
celery.config_from_object(celery_config)

#celery.conf.update(
    #CELERYD_POOL='gevent',
    #CELERYD_CONCURRENCY=1
    #)
@celery.task(name='tasks.add')
def add(x, y, raise_exc=False):
    if raise_exc:
        raise Exception("test")
    return x + y

@celery.task(name='tasks.minus')
def minus(x, y):
    def callback(ret):
        print ret
    _minus.apply_async(args=(x,y),
                       link=callback)

@celery.async(name='tasks.minus.async')
def _minus(x, y):
    return x - y
