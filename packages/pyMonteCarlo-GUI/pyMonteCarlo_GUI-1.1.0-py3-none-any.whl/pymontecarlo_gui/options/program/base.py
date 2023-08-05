""""""

# Standard library modules.
import abc
import tempfile

# Third party modules.
from qtpy import QtGui
from unsync import unsync

# Local modules.
from pymontecarlo.util.error import ErrorAccumulator

from pymontecarlo_gui.widgets.field import WidgetFieldBase, CheckFieldBase
from pymontecarlo_gui.widgets.label import LabelIcon

# Globals and constants variables.


class ProgramFieldBase(WidgetFieldBase):

    _subclasses = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._subclasses.append(cls)

    def __init__(self, model):
        """
        Base class for all programs.

        :arg default_program: instance of the program
        """
        super().__init__()

        self.model = model

    def isValid(self):
        return super().isValid() and bool(self.programs())

    @abc.abstractmethod
    def programs(self):
        """
        Returns a :class:`list` of :class:`Program`.
        """
        return []


class CheckProgramField(CheckFieldBase):
    def __init__(self, program_field):
        self._program_field = program_field
        super().__init__()

    def title(self):
        return self.programField().title()

    def programField(self):
        return self._program_field


class ProgramsField(WidgetFieldBase):
    def __init__(self):
        super().__init__()

    def title(self):
        return "Program(s)"

    def isValid(self):
        # Selected fields
        selection = set(field for field in self.fields() if field.isChecked())
        if not selection:
            return False

        # Check field and program field must be valid
        for field in selection:
            # if not field.isValid():
            #     return False
            if not field.programField().isValid():
                return False

        return True

    def addProgramField(self, program_field):
        field = CheckProgramField(program_field)
        self.addCheckField(field)

    def selectedProgramFields(self):
        return set(field.programField() for field in self.fields() if field.isChecked())

    def programFields(self):
        return set(field.programField() for field in self.fields())

    def programs(self):
        programs = []
        for field in self.selectedProgramFields():
            programs.extend(field.programs())
        return programs
