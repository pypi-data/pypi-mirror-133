""""""

# Standard library modules.

# Third party modules.
import h5py

import numpy as np

from pypenelopetools.penelope.enums import ICOL

# Local modules.
import pymontecarlo.options.base as base
from pymontecarlo.options.particle import Particle

# Globals and constants variables.


class InteractionForcings(base.OptionBase):

    TOLERANCE = 1e-6

    def __init__(
        self,
        bremsstrahlung_xray_splitting_factor=1,
        characteristic_xray_splitting_factor=1,
    ):
        super().__init__()

        self._interactions = {}

        self.bremsstrahlung_xray_splitting_factor = bremsstrahlung_xray_splitting_factor
        self.characteristic_xray_splitting_factor = characteristic_xray_splitting_factor

    def __len__(self):
        return len(self._interactions)

    def __iter__(self):
        for (particle, collision), (
            forcer,
            weight_low,
            weight_high,
        ) in self._interactions.items():
            yield particle, collision, forcer, weight_low, weight_high

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and base.are_mapping_value_close(
                self._interactions, other._interactions, abs_tol=self.TOLERANCE
            )
            and base.isclose(
                self.bremsstrahlung_xray_splitting_factor,
                other.bremsstrahlung_xray_splitting_factor,
            )
            and base.isclose(
                self.characteristic_xray_splitting_factor,
                other.characteristic_xray_splitting_factor,
            )
        )

    def add(self, particle, collision, forcer, weight_low, weight_high):
        key = (particle, collision)
        if key in self._interactions:
            raise ValueError(
                "Interaction forcing for particle {} and collision {} already exists".format(
                    particle, collision
                )
            )

        self._interactions[key] = (forcer, weight_low, weight_high)

    def remove(self, particle, collision):
        self._interactions.pop((particle, collision))

    # region HDF5

    ATTR_BREMSSTRAHLUNG_XRAY_SPLITTING_FACTOR = "bremsstrahlung xray splitting factor"
    ATTR_CHARACTERISTIC_XRAY_SPLITTING_FACTOR = "characteristic xray splitting factor"
    DATASET_PARTICLE = "particle"
    DATASET_COLLISION = "collision"
    DATASET_FORCER = "forcer"
    DATASET_WEIGHT_LOW = "weight low"
    DATASET_WEIGHT_HIGH = "weight high"

    @classmethod
    def parse_hdf5(cls, group):
        bremsstrahlung_xray_splitting_factor = cls._parse_hdf5(
            group, cls.ATTR_BREMSSTRAHLUNG_XRAY_SPLITTING_FACTOR, int
        )
        characteristic_xray_splitting_factor = cls._parse_hdf5(
            group, cls.ATTR_CHARACTERISTIC_XRAY_SPLITTING_FACTOR, int
        )
        interactions = cls(
            bremsstrahlung_xray_splitting_factor, characteristic_xray_splitting_factor
        )

        particles = group[cls.DATASET_PARTICLE].asstr()
        collisions = group[cls.DATASET_COLLISION]
        forcers = group[cls.DATASET_FORCER]
        weights_low = group[cls.DATASET_WEIGHT_LOW]
        weights_high = group[cls.DATASET_WEIGHT_HIGH]

        for particle, collision, forcer, weight_low, weight_high in zip(
            particles, collisions, forcers, weights_low, weights_high
        ):
            particle = Particle[particle]
            collision = ICOL(collision)
            interactions.add(particle, collision, forcer, weight_low, weight_high)

        return interactions

    def convert_hdf5(self, group):
        super().convert_hdf5(group)

        self._convert_hdf5(
            group,
            self.ATTR_BREMSSTRAHLUNG_XRAY_SPLITTING_FACTOR,
            self.bremsstrahlung_xray_splitting_factor,
        )
        self._convert_hdf5(
            group,
            self.ATTR_CHARACTERISTIC_XRAY_SPLITTING_FACTOR,
            self.characteristic_xray_splitting_factor,
        )

        shape = (len(self),)

        dataset_particle = group.create_dataset(
            self.DATASET_PARTICLE, shape, dtype=h5py.special_dtype(vlen=str)
        )
        dataset_collision = group.create_dataset(
            self.DATASET_COLLISION, shape, dtype=int
        )
        dataset_forcer = group.create_dataset(self.DATASET_FORCER, shape, dtype=float)
        dataset_weight_low = group.create_dataset(
            self.DATASET_WEIGHT_LOW, shape, dtype=float
        )
        dataset_weight_high = group.create_dataset(
            self.DATASET_WEIGHT_HIGH, shape, dtype=float
        )

        for i, (particle, collision, forcer, weight_low, weight_high) in enumerate(
            self
        ):
            dataset_particle[i] = particle.name
            dataset_collision[i] = int(collision)
            dataset_forcer[i] = forcer
            dataset_weight_low[i] = weight_low
            dataset_weight_high[i] = weight_high

    # endregion

    # region Series

    def convert_series(self, builder):
        super().convert_series(builder)

        builder.add_column(
            "bremsstrahlung xray splitting factor",
            "bremms splitting",
            self.bremsstrahlung_xray_splitting_factor,
        )
        builder.add_column(
            "characteristic xray splitting factor",
            "charac splitting",
            self.bremsstrahlung_xray_splitting_factor,
        )

        for particle, collision, forcer, _weight_low, _weight_high in self:
            name = "{} - {}".format(particle, collision)
            builder.add_column(name, name, forcer)

    # endregion

    # region Document

    DESCRIPTION_INTERACTION_FORCINGS = "interaction forcings"
    TABLE_INTERACTION_FORCINGS = "interaction forcings"

    def convert_document(self, builder):
        super().convert_document(builder)

        description = builder.require_description(self.DESCRIPTION_INTERACTION_FORCINGS)
        description.add_item(
            "Bremmstrahlung X-ray splitting factor",
            self.bremsstrahlung_xray_splitting_factor,
        )
        description.add_item(
            "Characteristic X-ray splitting factor",
            self.characteristic_xray_splitting_factor,
        )

        table = builder.require_table(self.TABLE_INTERACTION_FORCINGS)
        table.add_column("Particle")
        table.add_column("Collision")
        table.add_column("Forcer")
        table.add_column("Weight Low")
        table.add_column("Weight High")

        for particle, collision, forcer, weight_low, weight_high in self:
            row = {
                "Particle": particle,
                "Collision": collision,
                "Forcer": forcer,
                "Weight Low": weight_low,
                "Weight High": weight_high,
            }
            table.add_row(row)


# endregion


class LazyInteractionForcings(base.LazyOptionBase):
    def apply(self, parent_option, options):
        interactions = InteractionForcings()

        if options.beam.particle == Particle.ELECTRON:
            interactions.add(
                Particle.ELECTRON, ICOL.HARD_BREMSSTRAHLUNG_EMISSION, -40, 1e-4, 1.0
            )
            interactions.add(
                Particle.ELECTRON, ICOL.INNER_SHELL_IMPACT_IONISATION, -40, 1e-4, 1.0
            )

        interactions.bremsstrahlung_xray_splitting_factor = 2
        interactions.characteristic_xray_splitting_factor = 2

        return interactions

    def convert_document(self, builder):
        super().convert_document(builder)

        text = (
            "Default interaction forcings created using "
            "a forcer of -40 for hard Bremsstrahlung emission and inner shell impact ionisation "
            "The Bremsstrahlung and characteristic X-ray splitting factor is set to 2"
        )
        builder.add_text(text)
