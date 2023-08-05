""""""

# Standard library modules.

# Third party modules.
import pyxray

# Local modules.
import pymontecarlo.options.base as base
from pymontecarlo.options.xrayline import LazyLowestEnergyXrayLine
from pymontecarlo.options.detector import PhotonDetector

# Globals and constants variables.


class ReferenceLine(base.OptionBase):

    RELATIVE_UNCERTAINTY_TOLERANCE = 1e-4  # 0.01%

    def __init__(self, xrayline, photon_detector, relative_uncertainty):
        super().__init__()

        self.xrayline = xrayline
        self.photon_detector = photon_detector
        self.relative_uncertainty = relative_uncertainty

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and base.isclose(self.xrayline, other.xrayline)
            and base.isclose(self.photon_detector, other.photon_detector)
            and base.isclose(
                self.relative_uncertainty,
                other.relative_uncertainty,
                abs_tol=self.RELATIVE_UNCERTAINTY_TOLERANCE,
            )
        )

    # region HDF5

    ATTR_XRAYLINE = "xray line"
    ATTR_PHOTON_DETECTOR = "photon detector"
    ATTR_RELATIVE_UNCERTAINTY = "relative uncertainty"

    @classmethod
    def parse_hdf5(cls, group):
        xrayline = cls._parse_hdf5(group, cls.ATTR_XRAYLINE, pyxray.XrayLine)
        photon_detector = cls._parse_hdf5(
            group, cls.ATTR_PHOTON_DETECTOR, PhotonDetector
        )
        relative_uncertainty = cls._parse_hdf5(
            group, cls.ATTR_RELATIVE_UNCERTAINTY, float
        )
        return cls(xrayline, photon_detector, relative_uncertainty)

    def convert_hdf5(self, group):
        super().convert_hdf5(group)
        self._convert_hdf5(group, self.ATTR_XRAYLINE, self.xrayline)
        self._convert_hdf5(group, self.ATTR_PHOTON_DETECTOR, self.photon_detector)
        self._convert_hdf5(
            group, self.ATTR_RELATIVE_UNCERTAINTY, self.relative_uncertainty
        )

    # endregion

    # region Series

    def convert_series(self, builder):
        super().convert_series(builder)
        builder.add_column("reference xray line", "ref xray", self.xrayline)
        builder.add_column(
            "reference photon detector", "ref detector", self.photon_detector.name
        )
        builder.add_column(
            "reference relative uncertainty",
            "ref 3sigma",
            self.relative_uncertainty,
            None,
            self.RELATIVE_UNCERTAINTY_TOLERANCE,
        )

    # endregion

    # region Document

    DESCRIPTION_REFERENCE_LINE = "reference line"

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description(self.DESCRIPTION_REFERENCE_LINE)
        description.add_item("X-ray line", self.xrayline)
        description.add_item("Photon detector", self.photon_detector.name)
        description.add_item(
            "Relative uncertainty",
            self.relative_uncertainty,
            None,
            self.RELATIVE_UNCERTAINTY_TOLERANCE,
        )


# endregion


class LazyReferenceLine(base.LazyOptionBase):

    RELATIVE_UNCERTAINTY_TOLERANCE = ReferenceLine.RELATIVE_UNCERTAINTY_TOLERANCE

    def __init__(self, xrayline=None, relative_uncertainty=0.05):
        super().__init__()
        self.relative_uncertainty = relative_uncertainty

        if xrayline is None:
            xrayline = LazyLowestEnergyXrayLine(minimum_energy_eV=100.0)
        self.xrayline = xrayline

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and base.isclose(
                self.relative_uncertainty,
                other.relative_uncertainty,
                abs_tol=self.RELATIVE_UNCERTAINTY_TOLERANCE,
            )
            and base.isclose(self.xrayline, other.xrayline)
        )

    def _find_detector(self, options):
        photon_detectors = options.find_detectors(PhotonDetector)
        if not photon_detectors:
            raise ValueError("No photon detector found")

        detector_elevations = {}
        for photon_detector in photon_detectors:
            detector_elevations[photon_detector.elevation_rad] = photon_detector

        return detector_elevations[min(detector_elevations.keys())]

    def apply(self, parent_option, options):
        # Check that x-ray line exists in material
        xrayline = self.xrayline
        if (
            hasattr(xrayline, "atomic_number")
            and xrayline.atomic_number not in options.sample.atomic_numbers
        ):
            minimum_energy_eV = xrayline.energy_eV or 100.0
            xrayline = LazyLowestEnergyXrayLine(minimum_energy_eV)

        xrayline = base.apply_lazy(xrayline, self, options)
        photon_detector = self._find_detector(options)
        relative_uncertainty = base.apply_lazy(self.relative_uncertainty, self, options)
        return ReferenceLine(xrayline, photon_detector, relative_uncertainty)

    # region HDF5

    ATTR_XRAYLINE = "xray line"
    ATTR_RELATIVE_UNCERTAINTY = "relative uncertainty"

    @classmethod
    def parse_hdf5(cls, group):
        xrayline = cls._parse_hdf5(group, cls.ATTR_XRAYLINE, pyxray.XrayLine)
        relative_uncertainty = cls._parse_hdf5(
            group, cls.ATTR_RELATIVE_UNCERTAINTY, float
        )
        return cls(xrayline, relative_uncertainty)

    def convert_hdf5(self, group):
        super().convert_hdf5(group)
        self._convert_hdf5(group, self.ATTR_XRAYLINE, self.xrayline)
        self._convert_hdf5(
            group, self.ATTR_RELATIVE_UNCERTAINTY, self.relative_uncertainty
        )

    # endregion

    # region Series

    def convert_series(self, builder):
        super().convert_series(builder)

    # endregion

    # region Document

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description(
            ReferenceLine.DESCRIPTION_REFERENCE_LINE
        )
        description.add_item("X-ray line", self.xrayline)
        description.add_item("Photon detector", "Lowest elevation photon detector")
        description.add_item(
            "Relative uncertainty",
            self.relative_uncertainty,
            None,
            self.RELATIVE_UNCERTAINTY_TOLERANCE,
        )


# endregion
