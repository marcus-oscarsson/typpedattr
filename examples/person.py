# -*- coding: utf-8 -*-
import _phome

from typedattr.type import Int, Float, Str
from typedattr.concurrent.event import EventLoop, on_event

class Person(object):
    name = Str('')
    length = Float(181.4, 0, 300) # default value, min, max
    age = Int(0, 0, 150) # default value, min, max

    def __init__(self, name, length, age):
        self.name = name
        self.length = length
        self.age = age

        on_event(self.age.value_change, call = self.on_age_change)

    def on_age_change(self, new_value):
        print('Age changed to %s' % new_value)

if __name__ == '__main__':
    p1 = Person('P1', 175, 23)

    print p1.name.value()
    print p1.length.value()
    print p1.age.value()

    p1.age = 37

    EventLoop.process_events()
