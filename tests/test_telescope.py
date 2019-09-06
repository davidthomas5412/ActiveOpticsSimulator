import os
import yaml
import batoid
import numpy as np
from aos.telescope import BendingTelescope, ZernikeTelescope, Telescope
from aos.state import BendingState, ZernikeState


def test_intra_extra():
    LSST_g_fn = os.path.join(batoid.datadir, "LSST", "LSST_g.yaml")
    config = yaml.safe_load(open(LSST_g_fn))
    optic = batoid.parse.parse_optic(config['opticalSystem'])
    tel = Telescope(optic)

    z1 = tel.intra.itemDict['LSST.LSSTCamera.Detector'].coordSys.origin[2]
    z2 = tel.extra.itemDict['LSST.LSSTCamera.Detector'].coordSys.origin[2]
    deltaZ = z2 - z1

    np.testing.assert_almost_equal(deltaZ, 3e-3)


def test_nominal():
    btel = BendingTelescope.nominal()
    bOutRadius = btel.optic.itemDict['LSST.M1'].outRadius

    ztel = ZernikeTelescope.nominal()
    zOutRadius = ztel.optic.itemDict['LSST.M1'].outRadius

    assert bOutRadius == 4.18
    assert zOutRadius == 4.18


def test_camx():
    bstate = BendingState()
    bstate['camx'] = 1e-6
    btel = BendingTelescope.nominal()
    btel.update(bstate)
    bcamx = btel.optic.itemDict['LSST.LSSTCamera'].coordSys.origin[0]

    assert bcamx == bstate['camx']

    zstate = ZernikeState()
    zstate['camx'] = 1e-6
    ztel = ZernikeTelescope.nominal()
    ztel.update(zstate)
    zcamx = ztel.optic.itemDict['LSST.LSSTCamera'].coordSys.origin[0]

    assert zcamx == zstate['camx']


def test_m2rx():
    state = BendingState()
    state['m2rx'] = np.deg2rad(1e-3)
    tel = BendingTelescope.nominal()
    tel.update(state)

    m2rx = tel.optic.itemDict['LSST.M2'].coordSys.rot
    ref = batoid.RotX(state['m2rx'])

    np.testing.assert_allclose(m2rx, ref)


def test_bending_mode_update():
    state = BendingState()
    state['m2rx'] = np.deg2rad(1e-3)
    state['m2b3'] = 1e-6
    tel = BendingTelescope.nominal()
    tel.update(state)

    m2rx = tel.optic.itemDict['LSST.M2'].coordSys.rot
    ref = batoid.RotX(state['m2rx'])
    np.testing.assert_allclose(m2rx, ref)

    pert = tel.optic.itemDict['LSST.M2'].surface.surfaces[1]
    np.testing.assert_allclose(pert.zs, tel.m2res.surfResidual)


def test_zernike_update():
    state = ZernikeState()
    state['m2z11'] = 100e-9
    tel = ZernikeTelescope.nominal()
    tel.update(state)

    pert = tel.optic.itemDict['LSST.M2'].surface.surfaces[1]

    assert pert.coef[11] == state['m2z11']
    assert pert.R_inner == tel.optic.itemDict['LSST.M2'].inRadius
    assert pert.R_outer == tel.optic.itemDict['LSST.M2'].outRadius