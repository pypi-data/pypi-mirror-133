""""""

# Standard library modules.
import os

# Third party modules.
import pytest
import pyxray

# Local modules.
from pymontecarlo_penepma.importer import PenepmaImporter

# Globals and constants variables.


@pytest.fixture
def importer():
    return PenepmaImporter()


@pytest.mark.asyncio
async def test_import(event_loop, importer, options, testdatadir):
    dirpath = os.path.join(testdatadir, "sim1")

    results = await importer.import_(options, dirpath)

    assert len(results) == 2

    result = results[0]
    assert len(result) == 7 + 5

    intensity = result[(29, "Ka1")]
    assert intensity.n == pytest.approx(2.861705e-6, rel=1e-4)
    assert intensity.s == pytest.approx(2.44e-6 / 3, rel=1e-4)

    intensity = result[(29, "Ka")]
    assert intensity.n == pytest.approx(2.861705e-6 + 1.040620e-6, rel=1e-4)

    intensity = result[(29, "K")]
    assert intensity.n == pytest.approx(
        2.861705e-6 + 1.040620e-6 + 2.601550e-7, rel=1e-4
    )
