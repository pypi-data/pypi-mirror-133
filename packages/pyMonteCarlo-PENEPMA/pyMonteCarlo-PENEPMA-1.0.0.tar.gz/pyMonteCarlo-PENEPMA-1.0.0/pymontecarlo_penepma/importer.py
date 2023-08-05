""""""

# Standard library modules.

# Third party modules.
from pypenelopetools.penepma.results import (
    PenepmaEmittedIntensityResult,
    PenepmaGeneratedIntensityResult,
)

# Local modules.
from pymontecarlo.options.program.importer import ImporterBase
from pymontecarlo.options.analysis import PhotonIntensityAnalysis, KRatioAnalysis
from pymontecarlo.results.photonintensity import (
    EmittedPhotonIntensityResultBuilder,
    GeneratedPhotonIntensityResultBuilder,
)

# Globals and constants variables.


class PenepmaImporter(ImporterBase):
    def __init__(self):
        super().__init__()

        self.import_analysis_methods[
            PhotonIntensityAnalysis
        ] = self._import_analysis_photonintensity
        self.import_analysis_methods[KRatioAnalysis] = self._import_analysis_kratio

    async def _import(self, options, dirpath, erracc):
        return self._run_importers(options, dirpath, erracc)

    def _import_analysis_photonintensity(self, options, analysis, dirpath, errors):
        # Find detector index
        detectors = options.detectors
        detector_index = detectors.index(analysis.detector) + 1

        # Read emitted intensities
        result = PenepmaEmittedIntensityResult(detector_index)
        result.read_directory(dirpath)

        emitted_builder = EmittedPhotonIntensityResultBuilder(analysis)

        for xrayline, intensity in result.total_intensities_1_per_sr_electron.items():
            emitted_builder.add_intensity(xrayline, intensity.n, intensity.s)

        # Read generated intensities
        result = PenepmaGeneratedIntensityResult()
        result.read_directory(dirpath)

        generated_builder = GeneratedPhotonIntensityResultBuilder(analysis)

        for xrayline, intensity in result.total_intensities_1_per_sr_electron.items():
            generated_builder.add_intensity(xrayline, intensity.n, intensity.s)

        return [emitted_builder.build(), generated_builder.build()]

    def _import_analysis_kratio(self, options, analysis, dirpath, errors):
        # Do nothing
        return []
