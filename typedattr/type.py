# -*- coding: utf-8 -*-
from .typebase import TypedAttribute, TypedAttributeFactory


class ValidationError(Exception):
    pass


class Int(TypedAttributeFactory):
    def __init__(self, default=0, min=0, max=65535, unit = None,
                 allow_none = False, delegate = None, meta_options = {}):

        super(Int, self).__init__(default, meta_options, delegate)
        self._min = min
        self._max = max
        self._allow_none = allow_none
        self._unit = unit

    def new_type(self):
        return IntType(self._default, self._min, self._max, self._allow_none,
                       self._delegate_factory, self._unit, self._meta_options)


class IntType(TypedAttribute):
    def __init__(self, default, min, max, allow_none = False, df = None,
                 unit = None, meta_options = {}):
        self._min = min
        self._max = max
        self._allow_none = allow_none
        self._unit = unit
        super(IntType, self).__init__(df, meta_options)

    # Implementation of abstract method from BaseType
    def _validate(self, value):
        if not isinstance(value, int):
            msg = 'Value is of type %s, expected int' % type(value)
            ValidationError(msg)

        if (not self._allow_none) and (value is None):
            msg = 'None is not a valid value for %s, allow_none = False' % self
            raise ValidationError(msg)

        if value < self._min or value > self._max:
            msg = 'Value %s is not within the valid range' % value
            msg += ' %s <= value <= %s' % (self._min, self._max)

            raise ValidationError(msg)

        return True


class Float(TypedAttributeFactory):
    def __init__(self, default=0, min=0, max=65535, allow_none = False,
                 delegate = None, unit=None, meta_options = {}):
        super(Float, self).__init__(default, meta_options, delegate)
        self._min = min
        self._max = max
        self._allow_none = allow_none
        self._unit = unit

    def new_type(self):
        return FloatType(self._default, self._min, self._max, self._allow_none,
                         self._delegate_factory, self._unit, self._meta_options)


class FloatType(TypedAttribute):
    def __init__(self, default, min, max, allow_none = False,
                 df = None, unit = None, meta_options = {}):
        self._min = min
        self._max = max
        self._allow_none = allow_none
        self._unit = unit
        super(FloatType, self).__init__(df, meta_options)

    # Implementation of abstract method from BaseType
    def _validate(self, value):
        if not isinstance(value, float):
            msg = 'Value is of type %s, expected float' % type(value)
            ValidationError(msg)

        if (not self._allow_none) and (value is None):
            msg = 'None is not a valid value for %s, allow_none = False' % self
            raise ValidationError(msg)

        if value < self._min or value > self._max:
            msg = 'Value %s is not within the valid range' % value
            msg += ' %s <= value <= %s' % (self._min, self._max)

            raise ValidationError(msg)

        return True

class Str(TypedAttributeFactory):
    def __init__(self, default = '', allow_none = False, delegate = None, meta_options = {}):
        super(Str, self).__init__(default, meta_options, delegate)
        self._allow_none = allow_none

    def new_type(self):
        return StrType(self._allow_none, self._delegate_factory, self._meta_options)


class StrType(TypedAttribute):
    def __init__(self, allow_none, delegate, meta_options):
        self._allow_none = allow_none
        super(StrType, self).__init__(delegate, meta_options)

    # Implementation of abstract method from BaseType
    def _validate(self, value):
        if not isinstance(value, str):
            msg = 'Value is of type %s, expected str' % type(value)
            ValidationError(msg)

        if (not self._allow_none) and (value is None):
            msg = 'None is not a valid value for %s, allow_none = False' % self
            raise ValidationError(msg)

        return True
