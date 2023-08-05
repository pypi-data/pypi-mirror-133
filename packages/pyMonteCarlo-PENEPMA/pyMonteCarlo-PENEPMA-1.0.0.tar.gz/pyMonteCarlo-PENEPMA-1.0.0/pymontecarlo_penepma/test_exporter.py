#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import pytest

from pypenelopetools.penelope.enums import KPAR
from pypenelopetools.penepma.input import PenepmaInput
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.material import Material as Penmaterial

# Local modules.
from pymontecarlo.util.error import ErrorAccumulator
from pymontecarlo.options.material import Material
from pymontecarlo.options.beam import PencilBeam
from pymontecarlo.options.sample import (
    InclusionSample,
    HorizontalLayerSample,
    VerticalLayerSample,
    SphereSample,
)
from pymontecarlo.exceptions import ProgramNotFound

from pymontecarlo_penepma.exporter import PenepmaExporter
from pymontecarlo_penepma.program import PenepmaProgram

# Globals and constants variables.


def _has_penepma():
    try:
        program = PenepmaProgram()
        program.executable  # Raise ProgramNotFound
    except ProgramNotFound:
        return False

    return True


@pytest.fixture
def exporter():
    return PenepmaExporter()


@pytest.fixture
def dry_run():
    return not _has_penepma()


@pytest.mark.asyncio
@pytest.mark.skipif(not _has_penepma(), reason="Requires material program")
async def test_exporter_write_material(event_loop, exporter, options, tmp_path):
    penmaterial = Penmaterial(
        name="test", composition={29: 0.5, 30: 0.5}, density_g_per_cm3=8.7
    )
    erracc = ErrorAccumulator()

    await exporter._write_material(penmaterial, options, tmp_path, erracc)

    assert tmp_path.joinpath(penmaterial.filename).exists()


def _test_export(
    outputdir, expected_number_materials, expected_number_modules, dry_run
):
    if dry_run:
        return

    # Test ini
    infilepath = outputdir.joinpath(PenepmaExporter.DEFAULT_IN_FILENAME)
    assert infilepath.exists()

    input = PenepmaInput()
    with open(infilepath, "r") as fp:
        input.read(fp)

    assert input.SKPAR.get()[0] == KPAR.ELECTRON

    # Test materials
    assert len(list(outputdir.glob("mat*.mat"))) == expected_number_materials

    # Test geometry
    geofilepath = outputdir.joinpath(PenepmaExporter.DEFAULT_GEO_FILENAME)
    assert geofilepath.exists()

    geometry = Geometry()
    material_lookup = dict(
        (index, None) for index in range(1, expected_number_materials + 1)
    )
    with open(geofilepath, "r") as fp:
        geometry.read(fp, material_lookup)

    assert len(geometry.get_modules()) == expected_number_modules


@pytest.mark.asyncio
async def test_exporter_beam_pencil(event_loop, exporter, options, tmp_path, dry_run):
    options.beam = PencilBeam(10e3)
    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 1, 1, dry_run)


@pytest.mark.asyncio
async def test_exporter_substrate(event_loop, exporter, options, tmp_path, dry_run):
    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 1, 1, dry_run)


@pytest.mark.asyncio
async def test_exporter_inclusion(event_loop, exporter, options, tmp_path, dry_run):
    mat1 = Material("Mat1", {79: 0.5, 47: 0.5}, 2.0)
    mat2 = Material("Mat2", {29: 0.5, 30: 0.5}, 3.0)
    options.sample = InclusionSample(mat1, mat2, 10e-6)

    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 2, 2, dry_run)


@pytest.mark.asyncio
async def test_exporter_horizontallayers(
    event_loop, exporter, options, tmp_path, dry_run
):
    mat1 = Material("Mat1", {79: 0.5, 47: 0.5}, 2.0)
    mat2 = Material("Mat2", {29: 0.5, 30: 0.5}, 3.0)
    options.sample = HorizontalLayerSample(mat1)
    options.sample.add_layer(mat2, 10e-9)

    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 2, 2, dry_run)


@pytest.mark.asyncio
async def test_exporter_horizontallayers_no_substrate(
    event_loop, exporter, options, tmp_path, dry_run
):
    mat1 = Material("Mat1", {79: 0.5, 47: 0.5}, 2.0)
    mat2 = Material("Mat2", {29: 0.5, 30: 0.5}, 3.0)
    options.sample = HorizontalLayerSample()
    options.sample.add_layer(mat1, 10e-9)
    options.sample.add_layer(mat2, 10e-9)

    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 2, 2, dry_run)


@pytest.mark.asyncio
async def test_exporter_verticallayers(
    event_loop, exporter, options, tmp_path, dry_run
):
    mat1 = Material("Mat1", {79: 0.5, 47: 0.5}, 2.0)
    mat2 = Material("Mat2", {29: 0.5, 30: 0.5}, 3.0)
    options.sample = VerticalLayerSample(mat1, mat1)
    options.sample.add_layer(mat2, 100e-6)

    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 3, 3, dry_run)
    # It should be only two materials, but for now the same material
    # may be exported several times.


@pytest.mark.asyncio
async def test_exporter_verticallayers_couple(
    event_loop, exporter, options, tmp_path, dry_run
):
    mat1 = Material("Mat1", {79: 0.5, 47: 0.5}, 2.0)
    mat2 = Material("Mat2", {29: 0.5, 30: 0.5}, 3.0)
    options.sample = VerticalLayerSample(mat1, mat2)

    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 2, 2, dry_run)


@pytest.mark.asyncio
async def test_exporter_sphere(event_loop, exporter, options, tmp_path, dry_run):
    mat1 = Material("Mat1", {79: 0.5, 47: 0.5}, 2.0)
    options.sample = SphereSample(mat1, 250e-6)

    await exporter.export(options, tmp_path, dry_run=dry_run)
    _test_export(tmp_path, 1, 1, dry_run)
