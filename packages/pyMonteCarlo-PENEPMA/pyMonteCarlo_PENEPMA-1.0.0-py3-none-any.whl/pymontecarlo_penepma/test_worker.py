""""""

# Standard library modules.
import asyncio

# Third party modules.
import pytest

# Local modules.
from pymontecarlo.exceptions import ProgramNotFound
from pymontecarlo.util.token import Token, TokenState
from pymontecarlo.simulation import Simulation
from pymontecarlo.options.material import Material
from pymontecarlo.options.sample import (
    SubstrateSample,
    HorizontalLayerSample,
    VerticalLayerSample,
    InclusionSample,
    SphereSample,
)

from pymontecarlo_penepma.program import PenepmaProgram
from pymontecarlo_penepma.worker import PenepmaWorker

# Globals and constants variables.


def _has_penepma():
    try:
        program = PenepmaProgram()
        program.executable  # Raise ProgramNotFound
    except ProgramNotFound:
        return False

    return True


if not _has_penepma():
    pytest.skip("PENEPMA cannot be executed", allow_module_level=True)


def _create_samples(number_layers=2):
    yield SubstrateSample(Material.pure(39))

    yield InclusionSample(Material.pure(39), Material.pure(40), 20e-9)

    sample = HorizontalLayerSample(Material.pure(39))
    for i in range(number_layers):
        sample.add_layer(Material.pure(50 + i), 20e-9)
    yield sample

    sample = VerticalLayerSample(Material.pure(39), Material.pure(40))
    for i in range(number_layers):
        sample.add_layer(Material.pure(40 + i), 20e-9)
    yield sample

    yield SphereSample(Material.pure(39), 20e-9)


@pytest.mark.asyncio
@pytest.mark.parametrize("sample", _create_samples())
async def test_penepma_worker(event_loop, options, sample, tmp_path):
    options.sample = sample

    worker = PenepmaWorker()
    token = Token("test")
    simulation = Simulation(options)
    outputdir = tmp_path

    await worker.run(token, simulation, outputdir)

    assert token.state == TokenState.DONE
    assert token.progress == 1.0
    assert token.status == "Done"
    assert len(simulation.results) == 2

    assert outputdir.joinpath("pe-geometry.rep").exists()
    assert outputdir.joinpath("penepma.dat").exists()
    assert outputdir.joinpath("penepma-res.dat").exists()
    assert outputdir.joinpath("dump1.dat").exists()
    assert outputdir.joinpath("pe-intens-01.dat").exists()
    assert outputdir.joinpath("pe-material.dat").exists()


@pytest.mark.asyncio
async def test_penepma_cancel(event_loop, options, tmp_path):
    # Increase number of electrons
    options.program.number_trajectories = 10000

    worker = PenepmaWorker()
    token = Token("test")
    simulation = Simulation(options)
    outputdir = tmp_path

    task = asyncio.create_task(worker.run(token, simulation, outputdir))

    await asyncio.sleep(0.5)

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        assert True, "Task was cancelled properly"
    else:
        assert False

    assert token.state == TokenState.CANCELLED
    assert token.progress == 1.0
    assert token.status == "Cancelled"
    assert len(simulation.results) == 0
