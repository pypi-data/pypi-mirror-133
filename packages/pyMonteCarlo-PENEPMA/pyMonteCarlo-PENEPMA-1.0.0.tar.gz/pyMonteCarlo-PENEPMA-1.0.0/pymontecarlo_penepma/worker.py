"""
PENEPMA worker
"""

# Standard library modules.
import os
import asyncio
import logging

logger = logging.getLogger(__name__)

# Third party modules.
from pypenelopetools.penepma.input import PenepmaInput
from pypenelopetools.penepma.results import PenepmaResult

# Local modules.
from pymontecarlo.options.program.worker import WorkerBase
from pymontecarlo.util.process import create_startupinfo, kill_process
from pymontecarlo.exceptions import WorkerError

# Globals and constants variables.


class PenepmaWorker(WorkerBase):
    async def _run(self, token, simulation, outputdir):
        options = simulation.options
        program = options.program

        # Export
        token.update(0.1, "Exporting simulation")
        await program.exporter.export(options, outputdir)

        # Run
        token.update(0.2, "Run simulation")

        infilepath = os.path.join(outputdir, program.exporter.DEFAULT_IN_FILENAME)
        with open(infilepath, "r") as fileobj:
            # Read targets
            penepma_input = PenepmaInput()
            penepma_input.read(fileobj)

            (target_time_s,) = penepma_input.TIME.get()

            (target_trajectories,) = penepma_input.NSIMSH.get()

            _izs1s200, _idet, target_uncertainty = penepma_input.REFLIN.get()
            if target_uncertainty is None:
                target_uncertainty = 1.0

            fileobj.seek(0)

            # Setup result reader
            result = PenepmaResult()

            # Launch simulation
            args = [program.executable]

            logger.debug("Launching %s", " ".join(args))

            kwargs = {}
            kwargs["stdin"] = fileobj
            kwargs["stdout"] = asyncio.subprocess.PIPE
            kwargs["stderr"] = asyncio.subprocess.DEVNULL
            kwargs["cwd"] = outputdir
            kwargs["startupinfo"] = create_startupinfo()

            process = await asyncio.create_subprocess_exec(*args, **kwargs)

            try:
                # Update token
                while True:
                    stdout = await process.stdout.readline()
                    stdout = stdout.decode("ascii").strip()
                    if not stdout:
                        break
                    logger.debug("Stdout: {}".format(stdout))

                    if stdout.startswith("Number of simulated showers ="):
                        try:
                            result.read_directory(outputdir)
                        except:
                            logger.exception("Error while reading results")
                            continue

                        current_time_s = result.simulation_time_s.n
                        progress_time = current_time_s / target_time_s

                        current_trajectories = result.simulated_primary_showers.n
                        progress_trajectories = (
                            current_trajectories / target_trajectories
                        )

                        current_uncertainty = result.reference_line_uncertainty.n
                        progress_uncertainty = (
                            target_uncertainty - current_uncertainty
                        ) / target_uncertainty

                        progress = max(
                            0.001,
                            progress_time,
                            progress_trajectories,
                            progress_uncertainty,
                        )
                        progress = 0.7 * progress + 0.2
                        token.update(progress, "Running...")
                    else:
                        token.update(0.2, stdout)

                returncode = await process.wait()
                if returncode != 0:
                    raise WorkerError("Error running PENEPMA")

            except asyncio.CancelledError:
                # Make sure the process is killed before raising CancelledError
                kill_process(process.pid)
                raise

        # Import
        token.update(0.9, "Importing results")

        simulation.results += await program.importer.import_(options, outputdir)

        return simulation
