# -*- coding: utf-8 -*-
"""
    celery.worker.kikyo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Kikyo's consumer service
"""

from __future__ import absolute_import
from celery.utils.threads import bgThread
from celery.five import Empty
from celery.utils.log import get_logger
from celery.app import app_or_default

logger = get_logger(__name__)


class Consumer(bgThread):
    def __init__(self, app, ready_queue, pool, callback=None, **kwargs):
        super(Consumer, self).__init__(self, **kwargs)
        self.app = app_or_default(app)
        self.ready_queue = ready_queue
        self.pool = pool
        self.callback = callback or self.apply_async

    def body(self):
        # block here until there is a task
        try:
            task = self.ready_queue.consume(timeout=1.0)
        except Empty:
            return

        try:
            self.callback(task)
        except Exception as exc:
            logger.error('kikyo.consumer callback raised exception %r',
                         exc, exc_info=True,
                         extra={'data': {'name': task.name}})

    def apply_async(self, task):
        """execute the task using pool"""
        target = self.app._async_tasks[task.name]
        self.pool.apply_local_async(target, task.args,
                                    task.kwargs,
                                    callbacks=task.callbacks,
                                    err_callbacks=task.err_callbacks,
                                    timeout_callbacks=task.timeout_callbacks,
                                    timeout=task.timeout)
