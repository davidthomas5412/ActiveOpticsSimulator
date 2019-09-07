from aos.simulator import WavefrontSimulator
from aos.estimator import WavefrontEstimator
from aos.metric import SumOfSquares
from aos.control import GainController
from aos.telescope import BendingTelescope
from aos.state import BendingState
from aos.solver import SensitivitySolver


def test_integration():
    telescope = BendingTelescope.nominal(band='g')
    simulator = WavefrontSimulator()
    estimator = WavefrontEstimator()
    solver = SensitivitySolver()
    metric = SumOfSquares()
    controller = GainController(metric, gain=0.3)
    fieldx, fieldy = 0, 0

    x = BendingState()
    # add 1 micron of the third bending mode to M2.
    x['m2b3'] = 1e-6
    telescope.update(x)
    wavefront = simulator.simulateWavefront(telescope.optic, fieldx, fieldy)
    yest = estimator.estimate(wavefront)
    xest = solver.solve(yest)
    xprime, xdelta = controller.nextState(xest)

    # start second iteration
    telescope.update(xdelta)
    wavefront = simulator.simulateWavefront(telescope.optic, fieldx, fieldy)
    yest = estimator.estimate(wavefront)
    xest = solver.solve(yest)
    xprime, xdelta = controller.nextState(xest)