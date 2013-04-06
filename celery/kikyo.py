#-*- coding=utf-8 -*-

from __future__ import absolute_import

from celery.five import items
from celery.worker.kqueue import KGroupQueue
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
        else:
            self.priority = enum(def_enums={
                'normal':0
            }, nonvalid=-1)

        if kconf:
            for key, value in items(kconf):
                self.queue.touch(key, *value)

        self.queue.touch('default', priority=self.priority[-1])

    def produce(self, qkey, task):
        return self.queue.put(task, key=qkey)
    
    def consume(self, block=True, timeout=None):
        return self.queue.get(block, timeout)

    def create_channel(self, qkey, rate_limits=None, *args, **kwargs):
        self.queue.touch(qkey, rate_limits, *args, **kwargs)
