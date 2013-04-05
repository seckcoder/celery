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
rate_limit = "200/s"
@celery.task(name='tasks.minus')
def minus(x, y, raise_exc=False):
    def callback(ret):
        pass
    _minus.apply_async(qkey="minus",args=(x,y),
                       link=callback,
                       touch=True,
                       rate_limit=rate_limit)
@celery.task(name='tasks.minus')
def multi_minus(x, y, num):
    for i in xrange(num):
        def callback(ret):
            pass
        _minus.apply_async(qkey="minus", args=(x,y),
                           link=callback,
                           touch=True,
                           rate_limit=rate_limit)

@celery.async(name='tasks.minus.async')
def _minus(x, y):
    # Note _minus can only be called on the worker side
    return x - y
