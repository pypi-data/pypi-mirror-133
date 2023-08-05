""""""

# Standard library modules.

# Third party modules.
import pytest

from pypenelopetools.penelope.enums import ICOL

# Local modules.
import pymontecarlo.util.testutil as testutil
from pymontecarlo.options.particle import Particle

from pymontecarlo_penepma.interactionforcings import InteractionForcings

# Globals and constants variables.


@pytest.fixture
def interactions():
    interactions = InteractionForcings(2, 3)
    interactions.add(Particle.ELECTRON, ICOL.HARD_ELASTIC, -3, 0.1, 0.5)
    interactions.add(Particle.POSITRON, ICOL.HARD_INELASTIC, -30, 0.5, 0.9)
    return interactions


def test_interactions(interactions):
    assert interactions.bremsstrahlung_xray_splitting_factor == 2
    assert interactions.characteristic_xray_splitting_factor == 3
    assert len(interactions) == 2


def test_interactions_hdf5(interactions, tmp_path):
    testutil.assert_convert_parse_hdf5(interactions, tmp_path)


def test_interactions_copy(interactions):
    testutil.assert_copy(interactions)


def test_interactions_pickle(interactions):
    testutil.assert_pickle(interactions)


def test_interactions_series(interactions, seriesbuilder):
    interactions.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 4


def test_interactions_document(interactions, documentbuilder):
    interactions.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 8
