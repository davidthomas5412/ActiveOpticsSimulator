import os
import aos
import numpy as np
from aos.telescope import BendingTelescope
from aos.simulator import DonutSimulator, OPDSimulator


def test_opd_simulator():
    tel = BendingTelescope.nominal()
    sim = OPDSimulator()
    fieldx = 0
    fieldy = 0
    opd = sim.simulate(tel.optic, fieldx, fieldy)
    array = np.array(opd.array)

    ref = np.load(os.path.join(aos.testDir, 'nominal_opd_0_0.npy'))

    np.testing.assert_allclose(array, ref)


def test_donut_simulator():
    """
    import os
    import aos
    import numpy as np
    from aos.telescope import Telescope
    from aos.simulator import DonutSimulator, OPDSimulator

    np.random.seed(0)
    tel = Telescope.nominal()
    optic = tel.optic
    optic = optic.withGloballyShiftedOptic('LSST.LSSTCamera.Detector', [0, 0, -1.5e-3])
    sim = DonutSimulator()
    fieldx = 0
    fieldy = 0
    donut = sim.simulate(optic, fieldx, fieldy)
    donut = sim.simulate(optic, fieldx, fieldy)
    array = np.array(donut.array)
    np.save(os.path.join(aos.testDir, 'nominal_donut_0_0.npy'), array)
    """
    tel = BendingTelescope.nominal()
    sim = DonutSimulator()
    fieldx = 0
    fieldy = 0
    donut = sim.simulate(tel.intra, fieldx, fieldy)
    array = np.array(donut.array)

    ref = np.load(os.path.join(aos.testDir, 'nominal_donut_0_0.npy'))

    err = np.sum(np.abs(array - ref))
    poisson_err = np.sum(np.sqrt(ref))

    assert err < 2 * poisson_err