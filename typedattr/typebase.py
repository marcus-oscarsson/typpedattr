# -*- coding: utf-8 -*-
import weakref

from .concurrent.event import Event
from .concurrent.task import async_task, Lock


class ValidationError(Exception):
    pass


class ValueDelegateFactory(object):
    def __init__(self, init_value):
        super(ValueDelegateFactory, self).__init__()
        self._init_value = init_value
        self._owning_object = None

    def new_delegate(self):
        return ValueDelegate(self._init_value)

    def set_owner(self, obj):
        self._owning_object = obj


class TypedAttributeFactory(object):
    def __init__(self, default, meta_options, delegate_factory = None):
        super(TypedAttributeFactory, self).__init__()

        if not delegate_factory:
            delegate_factory = ValueDelegateFactory(default)

        self._delegate_factory = delegate_factory

        # We are using WeakValueDictionary here to make sure that 'unused'
        # values are removed by the garbage collector
        self.__values = weakref.WeakValueDictionary()

        self._meta_options = meta_options
        self._default = default

    def __get__(self, obj, objtype):
        return self._get_typped_attr(obj)

    def __set__(self, obj, value):
        typed_attr = self._get_typped_attr(obj)
        typed_attr.set_value(value, wait=True)

    def __delete__(self, obj):
        pass

    def _get_typped_attr(self, obj):
        if obj not in self.__values:
            self._delegate_factory.set_owner(obj)
            attr = self.new_type()
            self.__values[obj] = attr

        return self.__values[obj]

    #Abstract
    def new_type(self):
        raise NotImplementedError()


class ValueDelegate(object):
    def __init__(self, init_value):
        super(ValueDelegate, self).__init__()
        self._value = init_value

    def get_value(self):
        return self._value

    # This function needs to be thread safe or called in a thread safe manner 
    def set_value(self, value):
        if value != self._value:
            self._value = value

        return self._value


class TypedAttribute(object):
    value_change = Event()
    value_is_changing = Event()
    value_change_error = Event()

    def __init__(self, delegate_factory, meta_options):
        # Create the actual delegate
        self.meta_options = meta_options
        self._delegate = delegate_factory.new_delegate()
        self._rw_lock = Lock()

    # We might have several threads or co-routines executing this segment
    # so we need to make sure to lock it.
    @async_task
    def set_value(self, value):
        current_value = self.value()
        actual_value = None

        if value != current_value:
            with self._rw_lock:
                self.value_is_changing.fire(value)

                # Validate the value and actual_value, they might be incorrect!,
                # fire the value_change_error when something goes wrong
                try:
                    self.validate(value)

                    # Ask the delegate to set the value, the actual value is
                    # returned by the delegate.
                    actual_value = self._delegate.set_value(value)
                    self.validate(actual_value)
                except ValidationError as ex:
                    self.value_change_error.fire(ex)
                except Exception as ex:
                    self.value_change_error.fire(ex)
                else:
                    self.value_change.fire(actual_value)

        return actual_value

    @async_task
    def value(self):
        with self._rw_lock:
            return self._delegate.get_value()

    def validate(self, value = None):
        return self._validate(value)

    def _validate(self, value):
        raise NotImplementedError()
