""""""

# Standard library modules.
from operator import attrgetter
import itertools

# Third party modules.
from qtpy import QtCore, QtWidgets

# Local modules.
from pymontecarlo_gui.widgets.field import (
    FieldBase,
    MultiValueFieldBase,
    WidgetFieldBase,
)
from pymontecarlo_gui.widgets.lineedit import ColoredMultiFloatLineEdit
from pymontecarlo_gui.widgets.xrayline import XrayLineField
from pymontecarlo_gui.options.program.base import ProgramFieldBase

from pymontecarlo.options.xrayline import find_known_xray_lines
from pymontecarlo.options.detector import PhotonDetector
from pymontecarlo.options.base import apply_lazy

from pymontecarlo_penepma.program import PenepmaProgram, PenepmaProgramBuilder
from pymontecarlo_penepma.referenceline import LazyReferenceLine
from pymontecarlo_penepma.simulationparameters import LazySimulationParameters

# Globals and constants variables.


class ReferenceLineField(XrayLineField):
    def __init__(self, model):
        super().__init__(model.settings)

        # Variables
        self.model = model

        # Signals
        model.samplesChanged.connect(self._on_model_changed)
        model.beamsChanged.connect(self._on_model_changed)

    def _on_model_changed(self):
        if not self.model.builder.beams or not self.model.builder.samples:
            self.setXrayLines([])
            return

        # Find maximum beam energy
        maximum_energy_eV = max(
            apply_lazy(beam.energy_eV, beam, None) for beam in self.model.builder.beams
        )

        # Find all atomic numbers
        zs = set()
        for sample in self.model.builder.samples:
            zs.update(sample.atomic_numbers)

        # Extract x-ray lines
        xraylines = find_known_xray_lines(
            zs, minimum_energy_eV=0.0, maximum_energy_eV=maximum_energy_eV
        )

        # Sort by energy
        xraylines.sort(key=attrgetter("energy_eV"))

        self.setXrayLines(xraylines)

    def title(self):
        return "Lowest energy\nX-ray line of interest"

    def description(self):
        return "Simulation is adjusted to only consider X-ray lines with an energy greater than the select X-ray line"


class TerminationFieldBase(MultiValueFieldBase):
    def __init__(self):
        super().__init__()

        # Widgets
        self._suffix = QtWidgets.QCheckBox("Use as termination")
        self._suffix.setChecked(False)

        # Signals
        self._suffix.stateChanged.connect(self._on_checked)

    def _on_checked(self):
        self.widget().setEnabled(self.suffixWidget().isChecked())
        self.fieldChanged.emit()

    def suffixWidget(self):
        return self._suffix

    def isValid(self):
        if not self.suffixWidget().isChecked():
            return True
        return super().isValid()

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.widget().setEnabled(self._suffix.isChecked())  # Opposite to normal use


class SimulationTimeTerminationField(TerminationFieldBase):
    def __init__(self):
        super().__init__()

        # Widgets
        self._widget = ColoredMultiFloatLineEdit()
        self._widget.setRange(1, float("inf"), 0)
        self._widget.setEnabled(False)

        # Signals
        self._widget.valuesChanged.connect(self.fieldChanged)

    def title(self):
        return "Simulation time [s]"

    def widget(self):
        return self._widget

    def simulationTimesSecond(self):
        if not self._suffix.isChecked():
            return [1e38]
        else:
            return self._widget.values()

    def setSimulationTimesSecond(self, simulation_times):
        self._suffix.setChecked(True)
        self._widget.setValues(simulation_times)


class NumberTrajectoriesTerminationField(TerminationFieldBase):
    def __init__(self):
        super().__init__()

        # Widgets
        self._widget = ColoredMultiFloatLineEdit()
        self._widget.setRange(1, float("inf"), 0)
        self._widget.setEnabled(False)

        # Signals
        self._widget.valuesChanged.connect(self.fieldChanged)

    def title(self):
        return "Number of trajectories"

    def widget(self):
        return self._widget

    def numbersTrajectories(self):
        if not self._suffix.isChecked():
            return [1e38]
        else:
            return self._widget.values()

    def setNumbersTrajectories(self, numbers_trajectories):
        self._suffix.setChecked(True)
        self._widget.setValues(numbers_trajectories)


class RelativeUncertaintyTerminationField(TerminationFieldBase):
    def __init__(self):
        super().__init__()

        # Widgets
        self._widget = ColoredMultiFloatLineEdit()
        self._widget.setRange(0.1, 100.0, 1)
        self._widget.setEnabled(True)
        self._widget.setValues([5.0])

        self._suffix.setChecked(True)

        # Signals
        self._widget.valuesChanged.connect(self.fieldChanged)

    def title(self):
        return "Relative uncertainty (%)"

    def description(self):
        return "Relative statistical uncertainty (3*sigma) of the intensity of the x-ray line"

    def widget(self):
        return self._widget

    def relativeUncertainties(self):
        if not self._suffix.isChecked():
            return []
        else:
            return tuple(value * 0.01 for value in self._widget.values())

    def setRelativeUncertainties(self, relative_uncertainties):
        self._suffix.setChecked(True)
        self._widget.setValues([value * 100.0 for value in relative_uncertainties])


class TerminationField(WidgetFieldBase):
    def __init__(self):
        super().__init__()

        self.field_simulation_time = SimulationTimeTerminationField()
        self.addLabelField(self.field_simulation_time)

        self.field_number_trajectories = NumberTrajectoriesTerminationField()
        self.addLabelField(self.field_number_trajectories)

        self.field_relative_uncertainty = RelativeUncertaintyTerminationField()
        self.addLabelField(self.field_relative_uncertainty)

    def title(self):
        return "Termination conditions"

    def isValid(self):
        # At least one termination condition should be selected
        has_termination = any(
            field.suffixWidget().isChecked() for field in self.fields()
        )
        return super().isValid() and has_termination

    def simulationTimesSecond(self):
        return self.field_simulation_time.simulationTimesSecond()

    def numbersTrajectories(self):
        return self.field_number_trajectories.numbersTrajectories()

    def relativeUncertainties(self):
        return self.field_relative_uncertainty.relativeUncertainties()


class CField(MultiValueFieldBase):
    def __init__(self, title):
        self._title = title
        super().__init__()

        # Widgets
        self._widget = ColoredMultiFloatLineEdit()
        self._widget.setRange(0.0, 0.2, 2)
        self._widget.setValues([0.2])

        # Signals
        self._widget.valuesChanged.connect(self.fieldChanged)

    def title(self):
        return self._title

    def description(self):
        return "Elastic scattering parameter"

    def widget(self):
        return self._widget

    def setValues(self, c1s):
        self._widget.setValues(c1s)

    def values(self):
        return self._widget.values()


class SimulationParametersField(WidgetFieldBase):
    def __init__(self):
        super().__init__()

        self.field_c1 = CField("C1")
        self.addLabelField(self.field_c1)

        self.field_c2 = CField("C2")
        self.addLabelField(self.field_c2)

    def title(self):
        return "Simulation parameters"

    def description(self):
        return "Applies to all materials"

    def c1s(self):
        return self.field_c1.values()

    def c2s(self):
        return self.field_c2.values()


class XraySplittingFactorField(MultiValueFieldBase):
    def __init__(self, title):
        self._title = title
        super().__init__()

        # Widgets
        self._widget = ColoredMultiFloatLineEdit()
        self._widget.setRange(1, float("inf"), 0)
        self._widget.setValues([2])

        # Signals
        self._widget.valuesChanged.connect(self.fieldChanged)

    def title(self):
        return self._title

    def widget(self):
        return self._widget

    def splittingFactors(self):
        return self._widget.values()


class InteractionForcing:
    def __init__(self, particle, collision, forcers, weight_low, weight_high):
        self.particle = particle
        self.collision = collision
        self.forcers = tuple(forcers)
        self.weight_low = weight_low
        self.weight_high = weight_high

    def __eq__(self, other):
        return self.particle == other.particle and self.collision == other.collision


class InteractionForcingsModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._interactionforcings = []

    def rowCount(self, parent=None):
        return len(self._interactionforcings)

    def columnCount(self, parent=None):
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()
        interactionforcing = self._interactionforcings[row]

        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                return str(interactionforcing.particle)
            elif column == 1:
                return str(interactionforcing.collision)
            elif column == 2:
                return ", ".join(
                    "{:0f}".format(forcer) for forcer in interactionforcing.forcers
                )
            elif column == 3:
                return "{:.4f}-{:.4f}".format(
                    interactionforcing.weight_low, interactionforcing.weight_high
                )

        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Particle"
            elif section == 1:
                return "Collision"
            elif section == 2:
                return "Forcer"
            elif section == 3:
                return "Weight"

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemFlags(super().flags(index))

    def interactionForcings(self):
        return tuple(self._interactionforcings)

    def addInteractionForcing(self, interactionforcing):
        if interactionforcing in self._interactionforcings:
            raise ValueError(
                "Interaction forcing for ({}, {}) already exists".format(
                    interactionforcing.particle, interactionforcing.collision
                )
            )

        self._interactionforcings.append(interactionforcing)
        self.modelReset.emit()

    def removeElement(self, z):
        if z not in self._composition:
            return
        self._composition.pop(z)
        self._update_composition_atomic()
        self.modelReset.emit()

    def clearElements(self):
        self._composition.clear()
        self._update_composition_atomic()
        self.modelReset.emit()

    def hasElements(self):
        return bool(self._composition)


class InteractionForcingsField(WidgetFieldBase):
    def __init__(self):
        super().__init__()

        self.bremsstrahlung_xray_splitting_factor_field = XraySplittingFactorField(
            "Bremsstrahlung X-ray splitting factor"
        )
        self.addLabelField(self.bremsstrahlung_xray_splitting_factor_field)

        self.characteristic_xray_splitting_factor_field = XraySplittingFactorField(
            "Characteristic X-ray splitting factor"
        )
        self.addLabelField(self.characteristic_xray_splitting_factor_field)

    def title(self):
        return "Interaction forcings"

    def description(self):
        return "Applies to all bodies"

    def bremsstrahlungXraySplittingFactors(self):
        return self.bremsstrahlung_xray_splitting_factor_field.splittingFactors()

    def characteristicXraySplittingFactors(self):
        return self.characteristic_xray_splitting_factor_field.splittingFactors()


class PenepmaProgramField(ProgramFieldBase):
    def __init__(self, model):
        super().__init__(model)

        self.field_xrayline = ReferenceLineField(self.model)
        self.addLabelField(self.field_xrayline)

        self.field_termination = TerminationField()
        self.addGroupField(self.field_termination)

        self.field_simulation_parameters = SimulationParametersField()
        self.addGroupField(self.field_simulation_parameters)

        self.field_interaction_forcings = InteractionForcingsField()
        self.addGroupField(self.field_interaction_forcings)

    def title(self):
        return "PENEPMA"

    def description(self):
        return "Version 2016\nCopyright (c) 2001-2016 Universitat de Barcelona\n(Xavier Llovet and Francesc Salvat)"

    def programs(self):
        builder = PenepmaProgramBuilder()

        xrayline = self.field_xrayline.selectedXrayLine()

        for simulation_time_s in self.field_termination.simulationTimesSecond():
            builder.add_simulation_time_s(simulation_time_s)

        for number_trajectories in self.field_termination.numbersTrajectories():
            builder.add_number_trajectories(number_trajectories)

        for relative_uncertainty in self.field_termination.relativeUncertainties():
            reference_line = LazyReferenceLine(xrayline, relative_uncertainty)
            builder.add_reference_line(reference_line)

        c1s = self.field_simulation_parameters.c1s()
        c2s = self.field_simulation_parameters.c2s()
        for c1, c2 in itertools.product(c1s, c2s):
            simulation_parameters = LazySimulationParameters(xrayline, c1, c2)
            builder.add_simulation_parameters(simulation_parameters)

        # print(builder.build())
        return super().programs() + builder.build()
