import numpy as np
from aos.estimator import WavefrontEstimator, InversionEstimator, ForwardModelEstimator
from aos.simulator import WavefrontSimulator
from aos.telescope import ZernikeTelescope


def test_wavefront_estimator_roundtrip():
    est = WavefrontEstimator()
    nZern = 22
    for i in range(1, nZern):
        coefs = np.zeros(nZern + 1)
        coefs[i] = 1
        img = est.evaluate(coefs)
        zest = est.estimate(img)
        np.testing.assert_allclose(zest, coefs, atol=1e-6)


def test_estimator_against_simulator():
    sim = WavefrontSimulator()
    est = WavefrontEstimator()
    zt = ZernikeTelescope.nominal()
    fx, fy = (1.28, 1.28)
    simImg = sim.simulateWavefront(zt.optic, fx, fy)
    zest = est.estimate(simImg, nZern=40)
    estImg = est.evaluate(zest)

    comb = np.abs(simImg-estImg)
    mask = ~np.isnan(comb)
    diff = np.sum(comb[mask])
    avgErr = diff / np.sum(mask)

    assert avgErr < 5e-9


def test_inversion_estimator():
    estimator = InversionEstimator()


def test_foward_modeling_estimator():
    estimator = ForwardModelEstimator()
