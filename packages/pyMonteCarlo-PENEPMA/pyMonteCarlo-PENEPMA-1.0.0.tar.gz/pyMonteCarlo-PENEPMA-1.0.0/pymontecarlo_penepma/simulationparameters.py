""""""

# Standard library modules.

# Third party modules.
import pyxray

# Local modules.
import pymontecarlo.options.base as base
from pymontecarlo.options.particle import Particle
from pymontecarlo.options.xrayline import LazyLowestEnergyXrayLine

# Globals and constants variables.


class SimulationParameters(base.OptionBase):

    C1_C2_TOLERANCE = 1e-3
    ENERGY_TOLERANCE_eV = 1e-2  # 0.01 eV

    def __init__(
        self, eabs_electron_eV, eabs_photon_eV, eabs_positron_eV, c1, c2, wcc_eV, wcr_eV
    ):
        super().__init__()

        self.eabs_electron_eV = eabs_electron_eV
        self.eabs_photon_eV = eabs_photon_eV
        self.eabs_positron_eV = eabs_positron_eV
        self.c1 = c1
        self.c2 = c2
        self.wcc_eV = wcc_eV
        self.wcr_eV = wcr_eV

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and base.isclose(
                self.eabs_electron_eV,
                other.eabs_electron_eV,
                abs_tol=self.ENERGY_TOLERANCE_eV,
            )
            and base.isclose(
                self.eabs_photon_eV,
                other.eabs_photon_eV,
                abs_tol=self.ENERGY_TOLERANCE_eV,
            )
            and base.isclose(
                self.eabs_positron_eV,
                other.eabs_positron_eV,
                abs_tol=self.ENERGY_TOLERANCE_eV,
            )
            and base.isclose(self.c1, other.c1, abs_tol=self.C1_C2_TOLERANCE)
            and base.isclose(self.c2, other.c2, abs_tol=self.C1_C2_TOLERANCE)
            and base.isclose(
                self.wcc_eV, other.wcc_eV, abs_tol=self.ENERGY_TOLERANCE_eV
            )
            and base.isclose(
                self.wcr_eV, other.wcr_eV, abs_tol=self.ENERGY_TOLERANCE_eV
            )
        )

    # region HDF5

    ATTR_EABS_ELECTRON = "absorption energy electron (eV)"
    ATTR_EABS_PHOTON = "absorption energy photon (eV)"
    ATTR_EABS_POSITRON = "absorption energy positron (eV)"
    ATTR_C1 = "c1"
    ATTR_C2 = "c2"
    ATTR_WCC = "wcc (eV)"
    ATTR_WCR = "wcr (eV)"

    @classmethod
    def parse_hdf5(cls, group):
        eabs_electron_eV = cls._parse_hdf5(group, cls.ATTR_EABS_ELECTRON, float)
        eabs_photon_eV = cls._parse_hdf5(group, cls.ATTR_EABS_PHOTON, float)
        eabs_positron_eV = cls._parse_hdf5(group, cls.ATTR_EABS_POSITRON, float)
        c1 = cls._parse_hdf5(group, cls.ATTR_C1, float)
        c2 = cls._parse_hdf5(group, cls.ATTR_C2, float)
        wcc_eV = cls._parse_hdf5(group, cls.ATTR_WCC, float)
        wcr_eV = cls._parse_hdf5(group, cls.ATTR_WCR, float)
        return cls(
            eabs_electron_eV, eabs_photon_eV, eabs_positron_eV, c1, c2, wcc_eV, wcr_eV
        )

    def convert_hdf5(self, group):
        super().convert_hdf5(group)
        self._convert_hdf5(group, self.ATTR_EABS_ELECTRON, self.eabs_electron_eV)
        self._convert_hdf5(group, self.ATTR_EABS_PHOTON, self.eabs_photon_eV)
        self._convert_hdf5(group, self.ATTR_EABS_POSITRON, self.eabs_positron_eV)
        self._convert_hdf5(group, self.ATTR_C1, self.c1)
        self._convert_hdf5(group, self.ATTR_C2, self.c2)
        self._convert_hdf5(group, self.ATTR_WCC, self.wcc_eV)
        self._convert_hdf5(group, self.ATTR_WCR, self.wcr_eV)

    # endregion

    # region Series

    def convert_series(self, builder):
        super().convert_series(builder)

        builder.add_column(
            "absorption energy electron",
            "eabs electron",
            self.eabs_electron_eV,
            "eV",
            self.ENERGY_TOLERANCE_eV,
        )
        builder.add_column(
            "absorption energy photon",
            "eabs photon",
            self.eabs_photon_eV,
            "eV",
            self.ENERGY_TOLERANCE_eV,
        )
        builder.add_column(
            "absorption energy positron",
            "eabs positron",
            self.eabs_positron_eV,
            "eV",
            self.ENERGY_TOLERANCE_eV,
        )
        builder.add_column("c1", "c1", self.c1, None, self.C1_C2_TOLERANCE)
        builder.add_column("c2", "c2", self.c2, None, self.C1_C2_TOLERANCE)
        builder.add_column("wcc", "wcc", self.wcc_eV, "eV", self.ENERGY_TOLERANCE_eV)
        builder.add_column("wcr", "wcr", self.wcr_eV, "eV", self.ENERGY_TOLERANCE_eV)

    # endregion

    # region Document

    DESCRIPTION_SIMULATION_PARAMETERS = "simulation parameters"

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description(
            self.DESCRIPTION_SIMULATION_PARAMETERS
        )
        description.add_item(
            "Absorption energy of electrons",
            self.eabs_electron_eV,
            "eV",
            self.ENERGY_TOLERANCE_eV,
        )
        description.add_item(
            "Absorption energy of photons",
            self.eabs_photon_eV,
            "eV",
            self.ENERGY_TOLERANCE_eV,
        )
        description.add_item(
            "Absorption energy of positrons",
            self.eabs_positron_eV,
            "eV",
            self.ENERGY_TOLERANCE_eV,
        )
        description.add_item("C1", self.c1, None, self.C1_C2_TOLERANCE)
        description.add_item("C2", self.c2, None, self.C1_C2_TOLERANCE)
        description.add_item("WCC", self.wcc_eV, "eV", self.ENERGY_TOLERANCE_eV)
        description.add_item("WCR", self.wcr_eV, "eV", self.ENERGY_TOLERANCE_eV)


# endregion


class LazySimulationParameters(base.LazyOptionBase):

    C1_C2_TOLERANCE = SimulationParameters.C1_C2_TOLERANCE

    def __init__(self, xrayline=None, c1=0.2, c2=0.2):
        super().__init__()

        if xrayline is None:
            xrayline = LazyLowestEnergyXrayLine(minimum_energy_eV=100)
        self.xrayline = xrayline
        self.c1 = c1
        self.c2 = c2

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and base.isclose(self.xrayline, other.xrayline)
            and base.isclose(self.c1, other.c1, abs_tol=self.C1_C2_TOLERANCE)
            and base.isclose(self.c2, other.c2, abs_tol=self.C1_C2_TOLERANCE)
        )

    def apply(self, parent_option, options):
        xrayline = base.apply_lazy(self.xrayline, self, options)
        c1 = base.apply_lazy(self.c1, self, options)
        c2 = base.apply_lazy(self.c2, self, options)
        beam_energy_eV = base.apply_lazy(options.beam.energy_eV, options.beam, options)
        beam_particle = base.apply_lazy(options.beam.particle, options.beam, options)

        xrayline_energy_eV = max(xrayline.energy_eV - 100, 0.0)

        if beam_particle == Particle.ELECTRON:
            eabs_electron_eV = eabs_photon_eV = xrayline_energy_eV
            eabs_positron_eV = beam_energy_eV
        elif beam_particle == Particle.PHOTON:
            eabs_electron_eV = eabs_photon_eV = eabs_positron_eV = xrayline_energy_eV
        elif beam_particle == Particle.POSITRON:
            eabs_electron_eV = beam_energy_eV
            eabs_photon_eV = eabs_positron_eV = xrayline_energy_eV
        else:
            eabs_electron_eV = eabs_photon_eV = eabs_positron_eV = beam_energy_eV

        return SimulationParameters(
            eabs_electron_eV=eabs_electron_eV,
            eabs_photon_eV=eabs_photon_eV,
            eabs_positron_eV=eabs_positron_eV,
            c1=c1,
            c2=c2,
            wcc_eV=xrayline_energy_eV,
            wcr_eV=xrayline_energy_eV,
        )

    # region HDF5

    ATTR_XRAYLINE = "xray line"
    ATTR_C1 = "c1"
    ATTR_C2 = "c2"

    @classmethod
    def parse_hdf5(cls, group):
        xrayline = cls._parse_hdf5(group, cls.ATTR_XRAYLINE, pyxray.XrayLine)
        c1 = cls._parse_hdf5(group, cls.ATTR_C1, float)
        c2 = cls._parse_hdf5(group, cls.ATTR_C2, float)
        return cls(xrayline, c1, c2)

    def convert_hdf5(self, group):
        super().convert_hdf5(group)
        self._convert_hdf5(group, self.ATTR_XRAYLINE, self.xrayline)
        self._convert_hdf5(group, self.ATTR_C1, self.c1)
        self._convert_hdf5(group, self.ATTR_C2, self.c2)

    # endregion

    # region Series

    def convert_series(self, builder):
        super().convert_series(builder)

    # endregion

    # region Document

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description(
            SimulationParameters.DESCRIPTION_SIMULATION_PARAMETERS
        )
        description.add_item("Lowest energy X-ray line", self.xrayline)
        description.add_item("C1", self.c1, None, self.C1_C2_TOLERANCE)
        description.add_item("C2", self.c2, None, self.C1_C2_TOLERANCE)


# endregion
