""""""

# Standard library modules.

# Third party modules.
import pytest

import pyxray

# Local modules.
from pymontecarlo_penepma.referenceline import ReferenceLine, LazyReferenceLine

import pymontecarlo.util.testutil as testutil
from pymontecarlo.options.detector import PhotonDetector

# Globals and constants variables.


@pytest.fixture
def referenceline():
    xrayline = pyxray.xray_line(13, "Ka1")
    photon_detector = PhotonDetector("det", 0.5, 0.6)
    return ReferenceLine(xrayline, photon_detector, 0.05)


def test_referenceline(referenceline):
    assert referenceline.xrayline == pyxray.xray_line(13, "Ka1")
    assert referenceline.photon_detector.name == "det"
    assert referenceline.relative_uncertainty == pytest.approx(0.05, abs=1e-4)


def test_referenceline_eq(referenceline):
    xrayline = pyxray.xray_line(13, "Ka1")
    photon_detector = PhotonDetector("det", 0.5, 0.6)
    assert referenceline == ReferenceLine(xrayline, photon_detector, 0.05)

    assert referenceline != ReferenceLine(
        pyxray.xray_line(14, "Ka1"), photon_detector, 0.05
    )
    assert referenceline != ReferenceLine(
        xrayline, PhotonDetector("det2", 0.5, 0.6), 0.05
    )
    assert referenceline != ReferenceLine(xrayline, photon_detector, 0.99)


def test_referenceline_hdf5(referenceline, tmp_path):
    testutil.assert_convert_parse_hdf5(referenceline, tmp_path)


def test_referenceline_copy(referenceline):
    testutil.assert_copy(referenceline)


def test_referenceline_pickle(referenceline):
    testutil.assert_pickle(referenceline)


def test_referenceline_series(referenceline, seriesbuilder):
    referenceline.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 3


def test_referenceline_document(referenceline, documentbuilder):
    referenceline.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 8


@pytest.fixture
def lazyreferenceline():
    return LazyReferenceLine()


def test_lazyreferenceline_apply(options, lazyreferenceline):
    referenceline = lazyreferenceline.apply(None, options)

    assert referenceline.xrayline == pyxray.xray_line(29, "Ll")
    assert referenceline.photon_detector.name == "xray"
    assert referenceline.relative_uncertainty == pytest.approx(0.05, abs=1e-4)


def test_lazyreferenceline_eq(lazyreferenceline):
    assert lazyreferenceline == LazyReferenceLine()
    assert lazyreferenceline == LazyReferenceLine(relative_uncertainty=0.05)

    assert lazyreferenceline != LazyReferenceLine(pyxray.xray_line(14, "Ka1"), 0.04)
    assert lazyreferenceline != LazyReferenceLine(pyxray.xray_line(14, "Ka1"))
    assert lazyreferenceline != LazyReferenceLine(relative_uncertainty=0.04)


def test_lazyreferenceline_hdf5(lazyreferenceline, tmp_path):
    testutil.assert_convert_parse_hdf5(lazyreferenceline, tmp_path)


def test_lazyreferenceline_copy(lazyreferenceline):
    testutil.assert_copy(lazyreferenceline)


def test_lazyreferenceline_pickle(referenceline):
    testutil.assert_pickle(referenceline)


def test_lazyreferenceline_series(lazyreferenceline, seriesbuilder):
    lazyreferenceline.convert_series(seriesbuilder)
    assert len(seriesbuilder.build()) == 0


def test_lazyreferenceline_document(lazyreferenceline, documentbuilder):
    lazyreferenceline.convert_document(documentbuilder)
    document = documentbuilder.build()
    assert testutil.count_document_nodes(document) == 8
