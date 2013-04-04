#-*- coding=utf-8 -*-

from __future__ import absolute_import

from celery.five import items
from celery.utils.kqueue import KGroupQueue
from celery.utils.enum import enum

class Kikyo(object):
    def __init__(self, kconf=None, priority=None):
        self.queue = KGroupQueue.make(qkey='Global')
        if priority:
            priority.setdefault('nonvalid', -1)
            nonvalid = priority['nonvalid']
            del priority['nonvalid']
            self.priority = enum(def_enums=priority,
                                 nonvalid=nonvalid)

        if kconf:
            for key, value in items(kconf):
                self.queue.touch(key, *value)

        self.queue.touch('default', priority=priority[-1])

    def prodouce(self, qkey, task):
        return self.queue.put(task, key=qkey)
    
    def consume(self, block=True, timeout=None):
        return self.queue.get(block, timeout)
