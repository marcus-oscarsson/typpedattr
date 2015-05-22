# -*- coding: utf-8 -*-
"""
"""
from PyQt5.QtWidgets import (QSpinBox, QDoubleSpinBox, QLineEdit,
                             QApplication, QWidget, QFormLayout)
from PyQt5.QtCore import QTimer
#from PyQt5.QtGui import QFormLayout
from ..concurrent.event import on_event, EventLoop
from ..concurrent.task import TaskManager
from ..typebase import TypedAttribute
from ..type import FloatType, IntType, StrType

def unwrap(obj):
    return obj.unwrap()

# This is probably more than a view and should eventually be moved,
# I thought that it could contain session management and so on ...
class Application(object):
    def __init__(self, args):
        self._app = QApplication(args)
        self._event_loop_timer = QTimer()
        self._event_loop_timer.timeout.connect(EventLoop.process_events)
        self._event_loop_timer.start(0)

    def execute(self):
        exit_code = self._app.exec_()
        TaskManager.wait_for_tasks()
        return exit_code

class QtLineEditView(QLineEdit):
    def __init__(self, model, parent = None):
        super(QtLineEditView, self).__init__(parent)
        on_event(model.value_change, call = self.model_value_change)
        self._model = model
        self.init_view(parent, model)
        
    def init_view(self, parent_view, model):
        self.editingFinished.connect(self.widget_value_changed)
        self.setEnabled(False)
        model.value(wait=False, cb = self.model_value_change)

        if self._model.meta_options:
            tooltip = self._model.meta_options.get('tooltip', '')
            self.setToolTip(tooltip)    
        
        self.show()

    def model_value_change(self, value):
        self.setEnabled(True)
        self.editingFinished.disconnect(self.widget_value_changed)
        self.setText(value)
        self.editingFinished.connect(self.widget_value_changed)

    def widget_value_changed(self):
        new_value = self.text()
        self._model.value_change.block(self.model_value_change)
        self._model.set_value(new_value, wait = False, cb = self.val_change_cb)

    def val_change_cb(self, result):
        pass
        
    def model_value_is_changing(self, requested_value):
        self.setEnabled(False)

    def model_value_change_error(self, ex):
        print ex


class QtSpinBoxView(QSpinBox):
    def __init__(self, model, parent=None):
        super(QtSpinBoxView, self).__init__(parent)
        on_event(model.value_change, call = self.model_value_change)
        on_event(model.value_is_changing, call = self.model_value_is_changing)
        on_event(model.value_change_error, call = self.model_value_change_error)
        self._model = model
        self.init_view(parent, model)

    def init_view(self, parent_view, model):
        self.setMinimum(model._min)
        self.setMaximum(model._max)
        self.setSuffix(model._unit)

        self.editingFinished.connect(self.widget_value_changed)
        #self.setValue(model.value())
        self.setEnabled(False)
        model.value(wait=False, cb = self.model_value_change)

        if self._model.meta_options:
            tooltip = self._model.meta_options.get('tooltip', '')
            self.setToolTip(tooltip)    

        self.show()

    def model_value_change(self, value):
        self.setEnabled(True)
        self.editingFinished.disconnect(self.widget_value_changed)
        self.setValue(value)
        self.editingFinished.connect(self.widget_value_changed)

    def widget_value_changed(self):
        new_value = self.value()
        self._model.set_value(new_value, wait = False, cb = self.val_change_cb)

    def val_change_cb(self, result):
        pass
        
    def model_value_is_changing(self, requested_value):
        self.setEnabled(False)

    def model_value_change_error(self, ex):
        print ex


class QtDoubleSpinBoxView(QDoubleSpinBox):
    def __init__(self, model, parent=None):
        super(QtDoubleSpinBoxView, self).__init__(parent)
        on_event(model.value_change, call = self.model_value_change)
        on_event(model.value_is_changing, call = self.model_value_is_changing)
        on_event(model.value_change_error, call = self.model_value_change_error)
        self._model = model
        self.init_view(parent, model)

    def init_view(self, parent_view, model):
        self.setMinimum(model._min)
        self.setMaximum(model._max)
        self.setSuffix(model._unit)

        self.editingFinished.connect(self.widget_value_changed)
        #self.setValue(model.value())
        self.setEnabled(False)
        model.value(wait=False, cb = self.model_value_change)

        if self._model.meta_options:
            tooltip = self._model.meta_options.get('tooltip', '')
            self.setToolTip(tooltip)    

        self.show()

    def model_value_change(self, value):
        self.setEnabled(True)
        self.editingFinished.disconnect(self.widget_value_changed)
        self.setValue(value)
        self.editingFinished.connect(self.widget_value_changed)

    def widget_value_changed(self):
        new_value = self.value()
        self._model.set_value(new_value, wait = False, cb = self.val_change_cb)

    def val_change_cb(self, result):
        pass
        
    def model_value_is_changing(self, requested_value):
        self.setEnabled(False)

    def model_value_change_error(self, ex):
        print ex


class QtFormView(QWidget):
    def __init__(self, parent=None):
        super(QtFormView, self).__init__(parent)
        self.form_layout = QFormLayout()    
        self.setLayout(self.form_layout)

    def add_row(self, label, widget):
        self.form_layout.addRow(label, widget)


def FormView(model, controller = None):
    form_view = QtFormView(parent = None)
    attributes = []

    for attr in dir(model):
        attr = getattr(model, attr)

        if isinstance(attr, TypedAttribute):
            attributes.append(attr)

    for attr in attributes:
        attr_view = None
        
        if isinstance(attr, IntType):
            attr_view = QtSpinBoxView(attr, parent = form_view)
        elif isinstance(attr, FloatType):
            attr_view = QtDoubleSpinBoxView(attr, parent = form_view)
        elif isinstance(attr, StrType):
            attr_view = QtLineEditView(attr, parent = form_view)
            
        label = ''

        if attr.meta_options:
            label = attr.meta_options.get('label', None) + ':'
            form_view.add_row(label, attr_view)

    return form_view
