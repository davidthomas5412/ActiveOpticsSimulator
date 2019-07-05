import batoid
import numpy as np
from aos.telescope import Telescope
from aos.state import OpticalState


def test_nominal():
    tel = Telescope.nominal()
    outRadius = tel.optic.itemDict['LSST.M1'].outRadius

    assert outRadius == 4.18


def test_camx():
    state = OpticalState()
    state['camx'] = 1e-6
    tel = Telescope.nominal()
    tel.update(state)

    camx = tel.optic.itemDict['LSST.LSSTCamera'].coordSys.origin[0]

    assert camx == state['camx']


def test_m2rx():
    state = OpticalState()
    state['m2rx'] = np.deg2rad(1e-3)
    tel = Telescope.nominal()
    tel.update(state)

    m2rx = tel.optic.itemDict['LSST.M2'].coordSys.rot
    ref = batoid.RotX(state['m2rx'])

    np.testing.assert_allclose(m2rx, ref)


def test_bending_mode_update():
    state = OpticalState()
    state['m2rx'] = np.deg2rad(1e-3)
    state['m2b3'] = 1e-6
    tel = Telescope.nominal()
    tel.update(state)

    m2rx = tel.optic.itemDict['LSST.M2'].coordSys.rot
    ref = batoid.RotX(state['m2rx'])
    np.testing.assert_allclose(m2rx, ref)

    pert = tel.optic.itemDict['LSST.M2'].surface.surfaces[1]
    np.testing.assert_allclose(pert.zs, tel.m2res.surfResidual)