# -*- coding: utf-8 -*-
import _phome

from typedattr.type import Int, Float, Str
from typedattr.view.qt5 import Application, FormView

# Create a model using 'typed attributes'
class Person(object):
    name = Str('A name', meta_options = {'label': 'Name', 'tooltip':'Name'})
    age = Int(43, 0, 150, meta_options = {'label': 'Age', 'tooltip':'Age'})
    size = Float(198, 300, meta_options = {'label': 'Size', 'tooltip':'Size'})
    
if __name__ == '__main__':
    import sys    
    app = Application(sys.argv)

    p1 = Person()

    # Display the same instance in two forms
    view1 = FormView(p1)
    view1.show()

    view2 = FormView(p1)
    view2.show()
 
    app.execute()
