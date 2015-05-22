# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool

# This import is not used in this module but imported from this module.
# The idea is that lock can be replaced by another locking mechanism, for
# instance for co-routines.
from threading import Lock

from .event import EventLoop

def add_callback_as_event(cb):
    import threading
    print("Adding EVENT %s from thread %s" % (cb, threading.current_thread()))

    def cb_fun(result):
        EventLoop.enqeue_event(cb, (result,), {})

    return cb_fun


class TaskManager(object):
    thread_pool = ThreadPool(2)

    @staticmethod
    def run_task(func, args = [], kwargs = {}, wait = True, cb = None):
        if not wait:
            tp = TaskManager.thread_pool

            if cb:
                cb = add_callback_as_event(cb)
                tp.apply_async(func, args = args, kwds = kwargs, callback = cb)
            else:
                tp.apply_async(func, args = args, kwds = kwargs)

            return None
        else:
            return func(*args, **kwargs)

    @staticmethod
    def wait_for_tasks():
        TaskManager.thread_pool.close()
        TaskManager.thread_pool.join()


def async_task(func):
    def _inthread(*args, **kwargs):
        wait = True
        cb = None

        if 'wait' in kwargs:
            wait = kwargs['wait']
            del kwargs['wait']

        if 'cb' in kwargs:
            cb = kwargs['cb']
            del kwargs['cb']

        return TaskManager.run_task(func, args, kwargs, wait = wait, cb = cb)

    return _inthread
