""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pymontecarlo_gui.widgets.field import WidgetFieldBase, CheckFieldBase

# Globals and constants variables.


class ModelCheckField(CheckFieldBase):
    def __init__(self, model):
        self._model = model
        super().__init__()

    def title(self):
        return self._model.fullname

    def description(self):
        return self._model.reference

    def model(self):
        return self._model


class ModelFieldBase(WidgetFieldBase):
    def addModel(self, model, checked=False):
        field = ModelCheckField(model)
        field.setChecked(checked)
        self.addCheckField(field)

    def selectedModels(self):
        return tuple(field.model() for field in self.fields() if field.isChecked())
