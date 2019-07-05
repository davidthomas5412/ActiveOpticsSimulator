import numpy as np
import galsim
import batoid
from aos.estimator import OPDEstimator, InversionEstimator, ForwardModelEstimator


def test_opd_estimator():
    nZern = 10
    z = np.zeros(nZern+1)
    z[5] = 1
    obscuration = 0.61
    zern = galsim.zernike.Zernike(z, R_inner=obscuration)
    nx = 256
    X,Y = np.meshgrid(np.linspace(-1, 1, nx),
                      np.linspace(-1, 1, nx))
    R = np.sqrt(X ** 2 + Y ** 2)
    mask = np.logical_and(R < 1, R > obscuration)
    Z = zern.evalCartesian(X, Y)
    array = np.ma.masked_array(Z, mask)
    opd = batoid.Lattice(array, np.eye(2))

    estimator = OPDEstimator(obscuration=obscuration, nZern=10)
    zest = estimator.estimate(opd)

    np.testing.assert_allclose(zest, z[1:], atol=1e-6)


def test_inversion_estimator():
    estimator = InversionEstimator()


def test_foward_modeling_estimator():
    estimator = ForwardModelEstimator()
