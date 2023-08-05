"""
ExporterBase to .in and .geo file
"""

# Standard library modules.
import os
import math
import asyncio
import tempfile
import shutil
import itertools
import logging

logger = logging.getLogger()

# Third party modules.
from pypenelopetools.penelope.enums import KPAR, ICOL
from pypenelopetools.penepma.input import PenepmaInput
from pypenelopetools.pengeom.geometry import Geometry
from pypenelopetools.pengeom.surface import cylinder, zplane, xplane, sphere
from pypenelopetools.pengeom.module import Module, SidePointer
from pypenelopetools.material import (
    Material as PenelopeMaterial,
    VACUUM as PENELOPE_VACUUM,
)
from pypenelopetools.penepma.utils import convert_xrayline_to_izs1s200

# Local modules.
from pymontecarlo.options.base import apply_lazy
from pymontecarlo.options.beam import PencilBeam, CylindricalBeam
from pymontecarlo.options.particle import Particle
from pymontecarlo.options.sample import (
    SubstrateSample,
    HorizontalLayerSample,
    VerticalLayerSample,
    InclusionSample,
    SphereSample,
)
from pymontecarlo.options.detector.photon import PhotonDetector
from pymontecarlo.options.analysis import PhotonIntensityAnalysis, KRatioAnalysis
from pymontecarlo.options.program.exporter import ExporterBase
from pymontecarlo.util.cbook import normalize_angle
from pymontecarlo.util.process import create_startupinfo

# Globals and constants variables.
PARTICLE_INDEX = {
    Particle.ELECTRON: KPAR.ELECTRON,
    Particle.PHOTON: KPAR.PHOTON,
    Particle.POSITRON: KPAR.POSITRON,
}

MAXIMUM_NUMBER_MATERIALS = 10
MAXIMUM_NUMBER_PHOTON_DETECTORS = 25


def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


class PenepmaExporter(ExporterBase):

    DEFAULT_IN_FILENAME = "options.in"
    DEFAULT_GEO_FILENAME = "sample.geo"

    def __init__(self):
        super().__init__()

        self._write_materials_lock = asyncio.Lock()

        self.dump_interval_s = 30
        self.random_seeds = (-10, 1)
        self.photon_detector_elevation_opening_rad = math.radians(10)
        self.photon_detector_azimuth_opening_rad = math.radians(15)

        self.beam_export_methods[PencilBeam] = self._export_beam_pencil
        self.beam_export_methods[CylindricalBeam] = self._export_beam_cylindrical

        self.sample_export_methods[SubstrateSample] = self._export_sample_substrate
        self.sample_export_methods[InclusionSample] = self._export_sample_inclusion
        self.sample_export_methods[
            HorizontalLayerSample
        ] = self._export_sample_horizontallayers
        self.sample_export_methods[
            VerticalLayerSample
        ] = self._export_sample_verticallayers
        self.sample_export_methods[SphereSample] = self._export_sample_sphere

        self.detector_export_methods[PhotonDetector] = self._export_detector_photon

        self.analysis_export_methods[
            PhotonIntensityAnalysis
        ] = self._export_analysis_photonintensity
        self.analysis_export_methods[KRatioAnalysis] = self._export_analysis_kratio

    def __getstate__(self):
        content = self.__dict__.copy()
        content.pop("_write_materials_lock", None)
        return content

    async def _export(self, options, dirpath, erracc, dry_run=False):
        # Initialize PENELOPE objects
        input = self._create_input(options)
        geometry = self._create_geometry(options)

        # Export sample
        dsmaxs = {}
        self._export_sample(options.sample, options, erracc, geometry, dsmaxs)
        index_lookup = geometry.indexify()

        # Maximum step length of electrons and positrons in each body.
        # This parameter is important only for thin bodies;
        # it should be given a value of the order of one tenth of the body thickness or less.
        for module, thickness_m in dsmaxs.items():
            index = index_lookup[module]
            input.DSMAX.add(index, thickness_m / 10.0)

        # Export the rest
        self._export_program(
            options.program, options, erracc, input, geometry, index_lookup
        )
        self._export_beam(options.beam, options, erracc, input)
        self._export_detectors(options.detectors, options, erracc, input)
        self._export_analyses(options.analyses, options, erracc, input)

        # Write files
        if not dry_run:
            # Write geometry file
            (geofilename,) = input.GEOMFN.get()
            geofilepath = os.path.join(dirpath, geofilename)
            with open(geofilepath, "w") as fileobj:
                geometry.write(fileobj, index_lookup)

            # Write material files
            async with self._write_materials_lock:
                await self._write_materials(options, dirpath, erracc, geometry)

            # Write in file
            infilepath = os.path.join(dirpath, self.DEFAULT_IN_FILENAME)
            with open(infilepath, "w") as fileobj:
                input.write(fileobj)

    def _create_input(self, options):
        input = PenepmaInput()

        input.TITLE.set("Options")

        input.GEOMFN.set(self.DEFAULT_GEO_FILENAME)

        input.DUMPTO.set("dump1.dat")
        input.DUMPP.set(self.dump_interval_s)
        input.RSEED.set(*self.random_seeds)

        return input

    def _create_geometry(self, options):
        return Geometry()

    async def _write_materials(self, options, dirpath, erracc, geometry):
        tasks = []
        for penmaterial in geometry.get_materials():
            if penmaterial is PENELOPE_VACUUM:
                continue
            coro = self._write_material(
                penmaterial, options, dirpath, erracc
            )  # pylint: disable=assignment-from-no-return
            tasks.append(
                asyncio.ensure_future(coro)
            )  # Use ensure_future instead of create_task to be compatible with qasync

        await asyncio.gather(*tasks)

    async def _write_material(self, penmaterial, options, dirpath, erracc):
        # Create material
        with tempfile.TemporaryFile("w+") as fileobj:
            penmaterial.write_input(fileobj)
            fileobj.seek(0)

            args = [options.program.material_executable]

            logger.debug("Launching %s", " ".join(args))

            kwargs = {}
            kwargs["stdin"] = fileobj
            kwargs["stdout"] = asyncio.subprocess.DEVNULL
            kwargs["stderr"] = asyncio.subprocess.DEVNULL
            kwargs["cwd"] = options.program.pendbase_directory
            kwargs["startupinfo"] = create_startupinfo()

            process = await asyncio.create_subprocess_exec(*args, **kwargs)
            returncode = await process.wait()

            if returncode != 0:
                exc = RuntimeError(
                    "Error creating material {}".format(penmaterial.name)
                )
                erracc.add_exception(exc)

        # Move material file to output directory
        srcfilepath = os.path.join(
            options.program.pendbase_directory, penmaterial.filename
        )
        shutil.move(srcfilepath, dirpath)

        logger.debug("Created {}".format(penmaterial.filename))

    def _export_material(self, material, options, erracc, index):
        self._validate_material(material, options, erracc)

        name = apply_lazy(material.name, material, options)
        filename = "mat{:02d}.mat".format(index)
        composition = apply_lazy(material.composition, material, options)
        density_g_per_cm3 = apply_lazy(material.density_g_per_cm3, material, options)
        penmaterial = PenelopeMaterial(
            name, composition, density_g_per_cm3, filename=filename
        )

        return penmaterial

    def _validate_program(self, program, options, erracc):
        super()._validate_program(program, options, erracc)

        # Simulation parameters
        simulation_parameters = apply_lazy(
            program.simulation_parameters, program, options
        )

        if simulation_parameters.eabs_electron_eV < 0.0:
            exc = ValueError(
                "Electron absorption energy must be greater or equal to 0.0"
            )
            erracc.add_exception(exc)
        if simulation_parameters.eabs_photon_eV < 0.0:
            exc = ValueError("Photon absorption energy must be greater or equal to 0.0")
            erracc.add_exception(exc)
        if simulation_parameters.eabs_positron_eV < 0.0:
            exc = ValueError(
                "Positron absorption energy must be greater or equal to 0.0"
            )
            erracc.add_exception(exc)

        if simulation_parameters.c1 < 0.0 or simulation_parameters.c1 > 0.2:
            exc = ValueError("C1 must be between [0.0, 0.2]")
            erracc.add_exception(exc)
        if simulation_parameters.c2 < 0.0 or simulation_parameters.c2 > 0.2:
            exc = ValueError("C2 must be between [0.0, 0.2]")
            erracc.add_exception(exc)

        if simulation_parameters.wcc_eV < 0.0:
            exc = ValueError("WCC energy must be greater or equal to 0.0")
            erracc.add_exception(exc)
        if simulation_parameters.wcr_eV < 0.0:
            exc = ValueError("WCR energy must be greater or equal to 0.0")
            erracc.add_exception(exc)

        # Interaction forcings
        # FIXME: PENEPMA calculations is WRONG with negative forcers,
        # since PENEPMA uses the absorption energy of electron and
        # photons to evaluate the mean free path. This skews the
        # interaction forcings when the absorption energies are not
        # equal to 50.0 eV.
        interaction_forcings = apply_lazy(
            program.interaction_forcings, program, options
        )

        for (
            particle,
            collision,
            forcer,
            weight_low,
            weight_high,
        ) in interaction_forcings:
            if particle not in PARTICLE_INDEX and not isinstance(particle, KPAR):
                exc = ValueError("Unknown particle: {}".format(particle))
                erracc.add_exception(exc)

            if not isinstance(collision, ICOL):
                exc = ValueError("Unknown collision: {}".format(collision))
                erracc.add_exception(exc)

            if abs(forcer) < 1:
                exc = ValueError(
                    "Absolute value of forcer must be greater or equal to 1"
                )
                erracc.add_exception(exc)

            if weight_low < 0 or weight_low > 1:
                exc = ValueError("Low weight must be between [0.0, 1.0]")
                erracc.add_exception(exc)

            if weight_high < 0 or weight_high > 1:
                exc = ValueError("High weight must be between [0.0, 1.0]")
                erracc.add_exception(exc)

            if weight_high <= weight_low:
                exc = ValueError("High weight must be greater than low weight")
                erracc.add_exception(exc)

        if interaction_forcings.bremsstrahlung_xray_splitting_factor < 1:
            exc = ValueError(
                "Bremsstrahlung X-ray splitting factor must be greater or equal to 1"
            )
            erracc.add_exception(exc)

        if interaction_forcings.characteristic_xray_splitting_factor < 1:
            exc = ValueError(
                "Characteristic X-ray splitting factor must be greater or equal to 1"
            )
            erracc.add_exception(exc)

        # Reference line
        reference_line = apply_lazy(program.reference_line, program, options)
        if reference_line is not None:
            if reference_line.relative_uncertainty <= 0.0:
                exc = ValueError("Relative uncertainty must be greater than 0")
                erracc.add_exception(exc)

        # Number of trajectories
        number_trajectories = apply_lazy(program.number_trajectories, program, options)

        if number_trajectories <= 0:
            exc = ValueError("Number of trajectories must be greater than 0")
            erracc.add_exception(exc)

        # Simulation time
        simulation_time_s = apply_lazy(program.simulation_time_s, program, options)

        if simulation_time_s <= 0:
            exc = ValueError("Simulation time must be greater than 0")
            erracc.add_exception(exc)

        # At least one termination condition should be selected
        if (
            reference_line is None
            and number_trajectories >= 1e38
            and simulation_time_s >= 1e38
        ):
            exc = ValueError("At least one termination condition should be specified")
            erracc.add_exception(exc)

    def _export_program(self, program, options, erracc, input, geometry, index_lookup):
        self._validate_program(program, options, erracc)

        # Simulation parameters
        simulation_parameters = apply_lazy(
            program.simulation_parameters, program, options
        )

        for penmaterial in geometry.get_materials():
            index = index_lookup[penmaterial]
            filename = penmaterial.filename
            input.materials.add(
                index,
                filename,
                eabs1=simulation_parameters.eabs_electron_eV,
                eabs2=simulation_parameters.eabs_photon_eV,
                eabs3=simulation_parameters.eabs_positron_eV,
                c1=simulation_parameters.c1,
                c2=simulation_parameters.c2,
                wcc=simulation_parameters.wcc_eV,
                wcr=simulation_parameters.wcr_eV,
            )

        # Interaction forcings
        interaction_forcings = apply_lazy(
            program.interaction_forcings, program, options
        )

        for module in geometry.get_modules():
            index = index_lookup[module]

            for (
                particle,
                collision,
                forcer,
                weight_low,
                weight_high,
            ) in interaction_forcings:
                if particle in Particle:
                    particle = PARTICLE_INDEX[particle]

                input.IFORCE.add(
                    index, particle, collision, forcer, weight_low, weight_high
                )

            if interaction_forcings.bremsstrahlung_xray_splitting_factor > 1:
                input.IBRSPL.add(
                    index, interaction_forcings.bremsstrahlung_xray_splitting_factor
                )

            if interaction_forcings.characteristic_xray_splitting_factor > 1:
                input.IXRSPL.add(
                    index, interaction_forcings.characteristic_xray_splitting_factor
                )

        # Reference line
        reference_line = apply_lazy(program.reference_line, program, options)

        if reference_line is not None:
            izs1s200 = convert_xrayline_to_izs1s200(reference_line.xrayline)

            photon_detectors = options.find_detectors(PhotonDetector)
            photon_detector = reference_line.photon_detector

            try:
                index_detector = photon_detectors.index(photon_detector) + 1
            except ValueError:
                exc = ValueError("Cannot find photon detector used in reference line")
                erracc.add_exception(exc)
                index_detector = 0

            relative_uncertainty = reference_line.relative_uncertainty

            input.REFLIN.set(izs1s200, index_detector, relative_uncertainty)

        # Number of trajectories
        number_trajectories = apply_lazy(program.number_trajectories, program, options)
        input.NSIMSH.set(number_trajectories)

        # Simulation time
        simulation_time_s = apply_lazy(program.simulation_time_s, program, options)
        input.TIME.set(simulation_time_s)

    def _validate_beam(self, beam, options, erracc):
        super()._validate_beam(beam, options, erracc)

        # Energy
        energy_eV = apply_lazy(beam.energy_eV, beam, options)

        if energy_eV < 100:
            exc = ValueError(
                "Energy ({} eV) must be greater than 100 eV".format(energy_eV)
            )
            erracc.add_exception(exc)

        if energy_eV > 1e9:
            exc = ValueError("Energy ({} eV) must be less than 1 GeV".format(energy_eV))
            erracc.add_exception(exc)

        # Particle
        particle = apply_lazy(beam.particle, beam, options)

        if particle not in PARTICLE_INDEX:
            exc = ValueError("Particle ({}) is not available".format(particle))
            erracc.add_exception(exc)

    def _export_beam_pencil(self, beam, options, erracc, input):
        self._validate_beam_pencil(beam, options, erracc)

        particle = apply_lazy(beam.particle, beam, options)
        input.SKPAR.set(PARTICLE_INDEX[particle])

        energy_eV = apply_lazy(beam.energy_eV, beam, options)
        input.SENERG.set(energy_eV)

        x0_m = apply_lazy(beam.x0_m, beam, options)
        y0_m = apply_lazy(beam.y0_m, beam, options)
        input.SPOSIT.set(x0_m * 1e2, y0_m * 1e2, 1.0)  # cm

        input.SRADI.set(0.0)  # cm

        input.SDIREC.set(180.0, 0.0)  # pointing downwards
        input.SAPERT.set(0.0)

    def _export_beam_cylindrical(self, beam, options, erracc, input):
        self._validate_beam_cylindrical(beam, options, erracc)

        particle = apply_lazy(beam.particle, beam, options)
        input.SKPAR.set(PARTICLE_INDEX[particle])

        energy_eV = apply_lazy(beam.energy_eV, beam, options)
        input.SENERG.set(energy_eV)

        x0_m = apply_lazy(beam.x0_m, beam, options)
        y0_m = apply_lazy(beam.y0_m, beam, options)
        input.SPOSIT.set(x0_m * 1e2, y0_m * 1e2, 1.0)  # cm

        diameter_m = apply_lazy(beam.diameter_m, beam, options)
        input.SRADI.set(diameter_m / 2 * 1e2)  # cm

        input.SDIREC.set(180.0, 0.0)  # pointing downwards
        input.SAPERT.set(0.0)

    def _validate_sample(self, sample, options, erracc):
        super()._validate_sample(sample, options, erracc)

        if len(options.sample.materials) > MAXIMUM_NUMBER_MATERIALS:
            exc = ValueError(
                "PENEPMA supports a maximum of {} materials.".format(
                    MAXIMUM_NUMBER_MATERIALS
                )
            )
            erracc.add_exception(exc)

    def _export_sample_substrate(self, sample, options, erracc, geometry, dsmaxs):
        self._validate_sample_substrate(sample, options, erracc)

        # Geometry
        surface_cylinder = cylinder(100)  # 100 cm radius
        surface_top = zplane(0.0)  # z = 0
        surface_bottom = zplane(-100)  # z = -100 cm

        material = apply_lazy(sample.material, sample, options)
        penmaterial = self._export_material(material, options, erracc, index=1)

        module = Module(penmaterial, "Substrate")
        module.add_surface(surface_cylinder, SidePointer.NEGATIVE)
        module.add_surface(surface_top, SidePointer.NEGATIVE)
        module.add_surface(surface_bottom, SidePointer.POSITIVE)

        geometry.title = "Substrate"
        geometry.add_module(module)
        geometry.tilt_rad = apply_lazy(sample.tilt_rad, sample, options)
        geometry.rotation_rad = apply_lazy(sample.azimuth_rad, sample, options)

    def _export_sample_inclusion(self, sample, options, erracc, geometry, dsmaxs):
        self._validate_sample_inclusion(sample, options, erracc)

        # Surface
        inclusion_diameter_m = apply_lazy(sample.inclusion_diameter_m, sample, options)

        surface_cylinder = cylinder(100.0)  # 100 cm radius
        surface_top = zplane(0.0)  # z = 0
        surface_bottom = zplane(-100.0)  # z = -100 cm
        surface_sphere = sphere(inclusion_diameter_m / 2.0 * 100.0)

        # Inclusion module
        inclusion_material = apply_lazy(sample.inclusion_material, sample, options)
        penmaterial = self._export_material(
            inclusion_material, options, erracc, index=1
        )

        module_inclusion = Module(penmaterial, "Inclusion")
        module_inclusion.add_surface(surface_top, SidePointer.NEGATIVE)
        module_inclusion.add_surface(surface_sphere, SidePointer.NEGATIVE)

        dsmaxs[module_inclusion] = inclusion_diameter_m

        # Substrate module
        substrate_material = apply_lazy(sample.substrate_material, sample, options)
        penmaterial = self._export_material(
            substrate_material, options, erracc, index=2
        )

        module_substrate = Module(penmaterial, "Substrate")
        module_substrate.add_surface(surface_cylinder, SidePointer.NEGATIVE)
        module_substrate.add_surface(surface_top, SidePointer.NEGATIVE)
        module_substrate.add_surface(surface_bottom, SidePointer.POSITIVE)
        module_substrate.add_module(module_inclusion)

        # Geometry
        geometry.title = "Inclusion"
        geometry.add_module(module_substrate)
        geometry.add_module(module_inclusion)
        geometry.tilt_rad = apply_lazy(sample.tilt_rad, sample, options)
        geometry.rotation_rad = apply_lazy(sample.azimuth_rad, sample, options)

    def _export_sample_horizontallayers(
        self, sample, options, erracc, geometry, dsmaxs
    ):
        self._validate_sample_horizontallayers(sample, options, erracc)

        layers = apply_lazy(sample.layers, sample, options)
        zpositions_m = sample.layers_zpositions_m

        # Surfaces
        surface_cylinder = cylinder(100)  # 100 cm radius

        surface_layers = [zplane(0.0)]
        for layer, (zmin_m, _zmax_m) in zip(layers, zpositions_m):
            surface = zplane(zmin_m * 100.0)
            surface_layers.append(surface)

        # Modules
        index = 0
        tmpgrouping = []
        for layer, (surface_top, surface_bottom) in zip(
            layers, _pairwise(surface_layers)
        ):
            material = apply_lazy(layer.material, layer, options)
            penmaterial = self._export_material(material, options, erracc, index)

            module = Module(penmaterial, "Layer {}".format(index))
            module.add_surface(surface_cylinder, SidePointer.NEGATIVE)
            module.add_surface(surface_top, SidePointer.NEGATIVE)
            module.add_surface(surface_bottom, SidePointer.POSITIVE)

            thickness_m = apply_lazy(layer.thickness_m, layer, options)
            dsmaxs[module] = thickness_m

            geometry.add_module(module)
            tmpgrouping.append((module, surface_bottom))

            index += 1

        if sample.has_substrate():
            surface_top = surface_layers[-1]
            surface_bottom = zplane(
                surface_top.shift.z_cm - 100
            )  # 100 cm below last layer

            substrate_material = apply_lazy(sample.substrate_material, sample, options)
            penmaterial = self._export_material(
                substrate_material, options, erracc, index
            )

            module = Module(penmaterial, "Substrate")
            module.add_surface(surface_cylinder, SidePointer.NEGATIVE)
            module.add_surface(surface_top, SidePointer.NEGATIVE)
            module.add_surface(surface_bottom, SidePointer.POSITIVE)

            geometry.add_module(module)
            tmpgrouping.append((module, surface_bottom))

        # Grouping
        # G0: s0, s2, m0, m1
        # G1: s0, s3, m2, g0
        # G2: s0, s4, m3, g1
        # etc.

        if len(tmpgrouping) <= 2:  # no grouping required if only 2 modules
            return

        module, surface_bottom = tmpgrouping[1]

        group = Module(PENELOPE_VACUUM, "grouping")
        group.add_surface(surface_cylinder, SidePointer.NEGATIVE)
        group.add_surface(surface_layers[0], SidePointer.NEGATIVE)  # top z = 0.0
        group.add_surface(surface_bottom, SidePointer.POSITIVE)
        group.add_module(tmpgrouping[0][0])  # m0
        group.add_module(module)  # m1

        geometry.add_module(group)

        for module, surface_bottom in tmpgrouping[2:]:
            oldgroup = group

            group = Module(PENELOPE_VACUUM, "grouping")
            group.add_surface(surface_cylinder, SidePointer.NEGATIVE)
            group.add_surface(surface_layers[0], SidePointer.NEGATIVE)  # top z = 0.0
            group.add_surface(surface_bottom, SidePointer.POSITIVE)
            group.add_module(module)
            group.add_module(oldgroup)

            geometry.add_module(group)

        geometry.title = "Horizontal layers"
        geometry.tilt_rad = apply_lazy(sample.tilt_rad, sample, options)
        geometry.rotation_rad = apply_lazy(sample.azimuth_rad, sample, options)

    def _export_sample_verticallayers(self, sample, options, erracc, geometry, dsmaxs):
        self._validate_sample_verticallayers(sample, options, erracc)

        layers = apply_lazy(sample.layers, sample, options)
        xpositions_m = sample.layers_xpositions_m

        # Surfaces
        surface_cylinder = cylinder(100)  # 100 cm radius

        surface_top = zplane(0.0)  # z = 0

        depth_m = apply_lazy(sample.depth_m, sample, options)
        if math.isfinite(depth_m):
            surface_bottom = zplane(-depth_m * 100.0)
        else:
            surface_bottom = zplane(-100.0)  # z = -100 cm

        surface_layers = []
        if layers:
            for layer, (xmin_m, _xmax_m) in zip(layers, xpositions_m):
                surface = xplane(xmin_m * 100.0)
                surface_layers.append(surface)

            _xmin_m, xmax_m = xpositions_m[-1]
            surface = xplane(xmax_m * 100.0)
            surface_layers.append(surface)

        else:
            surface = xplane(0.0)
            surface_layers.append(surface)

        # Modules
        index = 1

        ## Left substrate
        left_material = apply_lazy(sample.left_material, sample, options)
        penmaterial = self._export_material(left_material, options, erracc, index)

        module = Module(penmaterial, "Left substrate")
        module.add_surface(surface_cylinder, SidePointer.NEGATIVE)
        module.add_surface(surface_top, SidePointer.NEGATIVE)
        module.add_surface(surface_bottom, SidePointer.POSITIVE)
        module.add_surface(surface_layers[0], SidePointer.NEGATIVE)

        if math.isfinite(depth_m):
            dsmaxs[module] = depth_m

        geometry.add_module(module)
        index += 1

        ## Layers
        for layer, (surface_left, surface_right) in zip(
            layers, _pairwise(surface_layers)
        ):
            material = apply_lazy(layer.material, layer, options)
            penmaterial = self._export_material(material, options, erracc, index)

            module = Module(penmaterial, "Layer {}".format(index - 1))
            module.add_surface(surface_cylinder, SidePointer.NEGATIVE)
            module.add_surface(surface_top, SidePointer.NEGATIVE)
            module.add_surface(surface_bottom, SidePointer.POSITIVE)
            module.add_surface(surface_left, SidePointer.POSITIVE)
            module.add_surface(surface_right, SidePointer.NEGATIVE)

            thickness_m = apply_lazy(layer.thickness_m, layer, options)
            dsmaxs[module] = min(thickness_m, depth_m)

            geometry.add_module(module)
            index += 1

        ## Right substrate
        right_material = apply_lazy(sample.right_material, sample, options)
        penmaterial = self._export_material(right_material, options, erracc, index)

        module = Module(penmaterial, "Right substrate")
        module.add_surface(surface_cylinder, SidePointer.NEGATIVE)
        module.add_surface(surface_top, SidePointer.NEGATIVE)
        module.add_surface(surface_bottom, SidePointer.POSITIVE)
        module.add_surface(surface_layers[-1], SidePointer.POSITIVE)

        if math.isfinite(depth_m):
            dsmaxs[module] = depth_m

        geometry.title = "Vertical layers"
        geometry.add_module(module)
        geometry.tilt_rad = apply_lazy(sample.tilt_rad, sample, options)
        geometry.rotation_rad = apply_lazy(sample.azimuth_rad, sample, options)

    def _export_sample_sphere(self, sample, options, erracc, geometry, dsmaxs):
        self._validate_sample_sphere(sample, options, erracc)

        # Surfaces
        diameter_m = apply_lazy(sample.diameter_m, sample, options)
        radius_m = diameter_m / 2.0
        surface_sphere = sphere(radius_m * 100.0)

        # Modules
        material = apply_lazy(sample.material, sample, options)
        penmaterial = self._export_material(material, options, erracc, index=1)

        module = Module(penmaterial, "Sphere")
        module.add_surface(surface_sphere, SidePointer.NEGATIVE)
        module.shift.z_m = -radius_m

        dsmaxs[module] = diameter_m

        geometry.title = "Sphere"
        geometry.add_module(module)
        geometry.tilt_rad = apply_lazy(sample.tilt_rad, sample, options)
        geometry.rotation_rad = apply_lazy(sample.azimuth_rad, sample, options)

    def _validate_detector(self, detector, options, erracc):
        super()._validate_detector(detector, options, erracc)

        photon_detectors = options.find_detectors(PhotonDetector)
        if len(photon_detectors) > MAXIMUM_NUMBER_PHOTON_DETECTORS:
            exc = ValueError(
                "PENEPMA only supports up to {} photon detectors. {} are defined".format(
                    MAXIMUM_NUMBER_PHOTON_DETECTORS, len(photon_detectors)
                )
            )
            erracc.add_exception(exc)

    def _export_detector_photon(self, detector, options, erracc, input):
        self._validate_detector_photon(detector, options, erracc)

        # Azimuthal angles
        if isinstance(options.sample, (SubstrateSample, HorizontalLayerSample)):
            phi1 = 0
            phi2 = 360
        elif isinstance(options.sample, VerticalLayerSample):
            azimuth_deg = apply_lazy(detector.azimuth_deg, detector, options)
            azimuth_opening_deg = math.degrees(self.photon_detector_azimuth_opening_rad)
            phi1 = normalize_angle(math.radians(azimuth_deg - azimuth_opening_deg))
            phi2 = normalize_angle(math.radians(azimuth_deg + azimuth_opening_deg))
            phi1, phi2 = map(math.degrees, sorted([phi1, phi2]))
        else:
            phi1 = 0
            phi2 = 360

        # Elevation angles
        # Convert elevation angles (angle from the x-y plane) to theta angles used in PENEPMA,
        # defined as angle from the positive z-axis
        elevation_deg = apply_lazy(detector.elevation_deg, detector, options)
        elevation_opening_deg = math.degrees(self.photon_detector_elevation_opening_rad)
        theta1 = 90.0 - (elevation_deg + elevation_opening_deg)
        theta2 = 90.0 - (elevation_deg - elevation_opening_deg)

        # Energy windows
        # FIXME: Support spectrum
        # options.find_analyses(Spectrum, detector)
        ipsf = 0
        edel = 0.0
        edeu = options.beam.energy_eV
        nche = 10

        input.photon_detectors.add(theta1, theta2, phi1, phi2, ipsf, edel, edeu, nche)

    def _export_analysis_photonintensity(self, analysis, options, erracc, input):
        self._validate_analysis_photonintensity(analysis, options, erracc)

    def _export_analysis_kratio(self, analysis, options, erracc, input):
        self._validate_analysis_kratio(analysis, options, erracc)
