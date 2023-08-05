""""""

# Standard library modules.

# Third party modules.
import pytest
import pyxray

# Local modules.
from pymontecarlo_penepma.simulationparameters import (
    SimulationParameters,
    LazySimulationParameters,
)

import pymontecarlo.util.testutil as testutil
from pymontecarlo.options.particle import Particle

# Globals and constants variables.


@pytest.fixture
def simulationparameters():
    return SimulationParameters(1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3)


def test_simulationparameters(simulationparameters):
    assert simulationparameters.eabs_electron_eV == pytest.approx(1e3, abs=1e-4)
    assert simulationparameters.eabs_photon_eV == pytest.approx(2e3, abs=1e-4)
    assert simulationparameters.eabs_positron_eV == pytest.approx(3e3, abs=1e-4)
    assert simulationparameters.c1 == pytest.approx(0.1, abs=1e-4)
    assert simulationparameters.c2 == pytest.approx(0.2, abs=1e-4)
    assert simulationparameters.wcc_eV == pytest.approx(4e3, abs=1e-4)
    assert simulationparameters.wcr_eV == pytest.approx(5e3, abs=1e-4)


def test_simulationparameters_eq(simulationparameters):
    assert simulationparameters == SimulationParameters(
        1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3
    )

    assert simulationparameters != SimulationParameters(
        99, 2e3, 3e3, 0.1, 0.2, 4e3, 5e3
    )
    assert simulationparameters != SimulationParameters(
        1e3, 99, 3e3, 0.1, 0.2, 4e3, 5e3
    )
    assert simulationparameters != SimulationParameters(
        1e3, 2e3, 99, 0.1, 0.2, 4e3, 5e3
    )
    assert simulationparameters != SimulationParameters(
        1e3, 2e3, 3e3, 0.09, 0.2, 4e3, 5e3
    )
    assert simulationparameters != SimulationParameters(
        1e3, 2e3, 3e3, 0.1, 0.09, 4e3, 5e3
    )
    assert simulationparameters != SimulationParameters(
        1e3, 2e3, 3e3, 0.1, 0.2, 99, 5e3
    )
    assert simulationparameters != SimulationParameters(
        1e3, 2e3, 3e3, 0.1, 0.2, 4e3, 99
    )


def test_simulationparameters_hdf5(simulationparameters, tmp_path):
    testutil.assert_convert_parse_hdf5(simulationparameters, tmp_path)


def test_simulationparameters_copy(simulationparameters):
    testutil.assert_copy(simulationparameters)


def test_simulationparameters_pickle(simulationparameters):
    testutil.assert_pickle(simulationparameters)


def test_simulationparameters_series(simulationparameters, seriesbuilder):
    simulationparameters.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 7


def test_simulationparameters_document(simulationparameters, documentbuilder):
    simulationparameters.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 12


@pytest.fixture
def lazysimulationparameters():
    return LazySimulationParameters(c1=0.1, c2=0.15)


def test_simulationparameters_apply_electron(options, lazysimulationparameters):
    simulationparameters = lazysimulationparameters.apply(None, options)

    assert simulationparameters.eabs_electron_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.eabs_photon_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.eabs_positron_eV == pytest.approx(15e3, abs=1e-4)
    assert simulationparameters.c1 == pytest.approx(0.1, abs=1e-4)
    assert simulationparameters.c2 == pytest.approx(0.15, abs=1e-4)
    assert simulationparameters.wcc_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.wcr_eV == pytest.approx(711, abs=1e-4)


def test_simulationparameters_apply_photon(options, lazysimulationparameters):
    options.beam.particle = Particle.PHOTON
    simulationparameters = lazysimulationparameters.apply(None, options)

    assert simulationparameters.eabs_electron_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.eabs_photon_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.eabs_positron_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.c1 == pytest.approx(0.1, abs=1e-4)
    assert simulationparameters.c2 == pytest.approx(0.15, abs=1e-4)
    assert simulationparameters.wcc_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.wcr_eV == pytest.approx(711, abs=1e-4)


def test_simulationparameters_apply_positron(options, lazysimulationparameters):
    options.beam.particle = Particle.POSITRON
    simulationparameters = lazysimulationparameters.apply(None, options)

    assert simulationparameters.eabs_electron_eV == pytest.approx(15e3, abs=1e-4)
    assert simulationparameters.eabs_photon_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.eabs_positron_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.c1 == pytest.approx(0.1, abs=1e-4)
    assert simulationparameters.c2 == pytest.approx(0.15, abs=1e-4)
    assert simulationparameters.wcc_eV == pytest.approx(711, abs=1e-4)
    assert simulationparameters.wcr_eV == pytest.approx(711, abs=1e-4)


def test_lazysimulationparameters_eq(lazysimulationparameters):
    assert lazysimulationparameters == LazySimulationParameters(c1=0.1, c2=0.15)

    assert lazysimulationparameters != LazySimulationParameters()
    assert lazysimulationparameters != LazySimulationParameters(
        pyxray.xray_line(13, "Ka1"), c1=0.1, c2=0.15
    )
    assert lazysimulationparameters != LazySimulationParameters(c1=0.09, c2=0.15)
    assert lazysimulationparameters != LazySimulationParameters(c1=0.1, c2=0.09)


def test_lazysimulationparameters_hdf5(lazysimulationparameters, tmp_path):
    testutil.assert_convert_parse_hdf5(lazysimulationparameters, tmp_path)


def test_lazysimulationparameters_copy(lazysimulationparameters):
    testutil.assert_copy(lazysimulationparameters)


def test_lazysimulationparameters_pickle(lazysimulationparameters):
    testutil.assert_pickle(simulationparameters)


def test_lazysimulationparameters_series(lazysimulationparameters, seriesbuilder):
    lazysimulationparameters.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 0


def test_lazysimulationparameters_document(lazysimulationparameters, documentbuilder):
    lazysimulationparameters.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 8
