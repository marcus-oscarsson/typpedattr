# -*- coding: utf-8 -*-
import weakref

from Queue import Queue, Empty


def on_event(event_trigger, call = None):
    event_trigger.callbacks[call] = call


# Remove event should preferably not be used, at least not to
# temporarily remove an event, since its not 'safe' from a concurrent
# point of view. Use the block method of the event trigger instead !
def remove_event(event_trigger, handler):
    if handler in event_trigger.callbacks:
        event_trigger.callbacks.pop(handler)


class ChangeSet(object):
    def __init__(self, value, rvalue = None, pvalue = None):
        self.value = value
        self.rvalue = rvalue
        self.pvalue = pvalue


class Event(object):
    def __init__(self):
        super(Event, self).__init__
        self.__triggers = {}

    def __get__(self, obj, objtype):
        return self._get_trigger(obj)

    def __set__(self, obj, value):
        pass

    def __delete__(self, obj):
        pass

    def _get_trigger(self, obj):
        if obj not in self.__triggers:
            self.__triggers[obj] = EventTrigger(obj)

        return self.__triggers[obj]


class EventTrigger(object):
    def __init__(self, source):
        super(EventTrigger, self).__init__()
        # Using dict prevents the callback from being added twice
        # Using a WeakValueDictionary to make sure that no callbacks
        # linger after they are removed
        self.callbacks = weakref.WeakValueDictionary()
        self.blocked_callbacks = {}
        self.change_history = []
        self.source = source
        self.blocked = False

    def __get__(self, obj, objtype):
        return self

    def __set__(self, obj, value):
        pass

    def __delete__(self, obj):
        pass

    def block(self, cb):
        self.blocked_callbacks[cb] = cb

    def fire(self, change_set):
        # Handle this in a better way so that it does not grow endlessly 
        #self.change_history.append(change_set)

        if self.blocked == True:
            self.blocked = False
            return

        for cb in self.callbacks.values():
            if not cb in self.blocked_callbacks:
                EventLoop.enqeue_event(cb, (change_set,), {})
            else:
                self.blocked_callbacks.pop(cb)


class EventLoop(object):
    # Contains tuples on the form (callback_fun, args, kwargs)
    __event_cb_list = Queue(1000)

    @staticmethod
    def process_events():
        while not EventLoop.__event_cb_list.empty():
            try:
                cb, args, kwargs = EventLoop.__event_cb_list.get_nowait()
                cb(*args, **kwargs)
            except Empty:
                break

    @staticmethod
    def enqeue_event(func, args, kwargs):
        EventLoop.__event_cb_list.put((func, args, kwargs))
