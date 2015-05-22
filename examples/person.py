# -*- coding: utf-8 -*-
import _phome

from typedattr.type import Int, Float, Str
from typedattr.concurrent.event import EventLoop, on_event

# Create a person object with typed attributes, name, length, and age
# Float and Int are given (defualt value, min value and max value)
# Trying to set a value oustide of the permitted range sends the event
# value_change_error. Another possibility would be to raise an Exception
class Person(object):
    name = Str('')    
    length = Float(181.4, 0, 300)  # default-, min-, max-value
    age = Int(0, 0, 150) # default-, min-, max-value

    # Simple init
    def __init__(self, name, length, age):
        self.name = name
        self.length = length
        self.age = age

        #Registering to events
        on_event(self.age.value_change, call = self.on_age_change)
        on_event(self.age.value_change_error, call = self.on_value_change_error)

    def on_age_change(self, new_value):
        print('Age changed to %s' % new_value)

    def on_value_change_error(self, ex):
        print('Ouch, got: %s' % str(ex))

        
if __name__ == '__main__':
    p1 = Person('P1', 175, 23)

    print p1.name.value()
    print p1.length.value()
    print p1.age.value()

    p1.age = 37
    p1.age = 500

    EventLoop.process_events()
