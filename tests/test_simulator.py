import os
import aos
import pytest
import numpy as np
from aos.telescope import BendingTelescope
from aos.simulator import DonutSimulator, WavefrontSimulator


def test_wavefront_simulator():
    """
    import os
    import aos
    import numpy as np
    from aos.telescope import BendingTelescope
    from aos.simulator import WavefrontSimulator

    tel = BendingTelescope.nominal()
    sim = WavefrontSimulator()
    fieldx, fieldy = (0, 0)
    wavefront = sim.simulateWavefront(tel.optic, fieldx, fieldy)
    ref = np.save(os.path.join(aos.testDir, 'nominal_wavefront_0_0.npy'), wavefront)
    """
    tel = BendingTelescope.nominal()
    sim = WavefrontSimulator()
    fieldx, fieldy = (0, 0)
    wavefront = sim.simulateWavefront(tel.optic, fieldx, fieldy)
    ref = np.load(os.path.join(aos.testDir, 'nominal_wavefront_0_0.npy'))

    np.testing.assert_allclose(wavefront, ref)
    np.testing.assert_array_equal(wavefront.shape, [255, 255])


def test_even_wavefront_raises():
    with pytest.raises(ValueError):
        WavefrontSimulator(nx=250)


def test_donut_simulator():
    """
    import os
    import aos
    import numpy as np
    from aos.telescope import BendingTelescope
    from aos.simulator import DonutSimulator
    import matplotlib.pyplot as plt

    tel = BendingTelescope.nominal()
    sim = DonutSimulator()
    fieldx, fieldy = (0, 0)
    donut = sim.simulateDonut(tel.intra, fieldx, fieldy)
    array = np.array(donut.array)
    np.save(os.path.join(aos.testDir, 'nominal_donut_0_0.npy'), array)
    """
    tel = BendingTelescope.nominal()
    sim = DonutSimulator()
    fieldx, fieldy = (0, 0)
    donut = sim.simulateDonut(tel.intra, fieldx, fieldy)
    array = np.array(donut.array)

    ref = np.load(os.path.join(aos.testDir, 'nominal_donut_0_0.npy'))

    err = np.sum(np.abs(array - ref))
    poisson_err = np.sum(np.sqrt(ref))

    assert err < 2 * poisson_err
    np.testing.assert_array_equal(array.shape, [192, 192])


def test_odd_crop_raises():
    with pytest.raises(ValueError):
        DonutSimulator(crop=191)
