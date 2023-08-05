""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
import pymontecarlo.util.testutil as testutil
from pymontecarlo_penepma.program import PenepmaProgram
from pymontecarlo_penepma.simulationparameters import SimulationParameters
from pymontecarlo_penepma.interactionforcings import LazyInteractionForcings

# Globals and constants variables.


@pytest.fixture
def simulation_parameters():
    return SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3)


@pytest.fixture
def program(simulation_parameters):
    return PenepmaProgram(
        simulation_parameters=simulation_parameters,
        simulation_time_s=5,
        number_trajectories=6,
    )


def test_program(program, simulation_parameters):
    assert program.simulation_parameters == simulation_parameters
    assert program.interaction_forcings == LazyInteractionForcings()
    assert program.reference_line is None
    assert program.simulation_time_s == 5
    assert program.number_trajectories == 6


def test_program_eq(program):
    assert program != PenepmaProgram()


def test_program_hdf5(program, tmp_path):
    testutil.assert_convert_parse_hdf5(program, tmp_path)


def test_program_copy(program):
    testutil.assert_copy(program)


def test_program_pickle(program):
    testutil.assert_pickle(program)


def test_program_series(program, seriesbuilder):
    program.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 10


def test_program_document(program, documentbuilder):
    program.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 7
