# -*- coding: utf-8 -*-
"""
    celery.worker.kikyo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Kikyo's consumer service
"""

from __future__ import absolute_import
from celery.utils.threads import bgThread


class Consumer(bgThread):
    def __init__(self, ready_queue, pool, callback=None, **kwargs):
        super(Consumer, self).__init__(self, name="kikyo.consumer", **kwargs)
        self.ready_queue = ready_queue
        self.pool = pool
        self.callback = callback or self.apply_async
        self._quick_put = self.ready_queue.put

    def body(self):
        task = self.ready_queue.consume(timeout=1.0)
        self.callback(task)

    def apply_async(self, task):
        pass
