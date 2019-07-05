import numpy as np
from aos.telescope import Telescope
from aos.simulator import OPDSimulator


def test_opd_simulator():
    np.random.seed(0)
    tel = Telescope.nominal()
    sim = OPDSimulator()
    fieldx = 0
    fieldy = 0
    opd = sim.simulate(tel.optic, fieldx, fieldy)
    array = np.array(opd.array)

    ref = np.load('nominal_opd_0_0.npy')

    np.testing.assert_allclose(array, ref)