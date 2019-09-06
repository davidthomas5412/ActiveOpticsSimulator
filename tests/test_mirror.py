import pytest
import numpy as np
from aos.mirror import M1M3Residual, M2Residual


def test_nmodes():
    nModes = 10
    m1m3residual = M1M3Residual(nModes=nModes)
    m2residual = M2Residual(nModes=nModes)
    m1m3residual.applyBending(np.zeros(nModes))
    m2residual.applyBending(np.zeros(nModes))

    with pytest.raises(ValueError):
        m1m3residual.applyBending(np.zeros(nModes+1))

    with pytest.raises(ValueError):
        m2residual.applyBending(np.zeros(nModes + 1))


def test_apply_bending_modes():
    nModes = 2
    modes = np.zeros(nModes)
    ind = 1
    modes[ind] = 1
    m1m3residual = M1M3Residual(nModes=nModes)
    m2residual = M2Residual(nModes=nModes)
    m1m3residual.applyBending(modes)
    m2residual.applyBending(modes)

    np.testing.assert_allclose(m1m3residual.surfResidual, m1m3residual.bendingMatrix[ind])
    np.testing.assert_allclose(m2residual.surfResidual, m2residual.bendingMatrix[ind])


def test_bending_modes_accumulate():
    nModes = 2
    up1 = np.zeros(nModes)
    up2 = np.zeros(nModes)
    up1[0] = 1
    up2[1] = 1
    comb = np.ones(nModes)

    m1m3res = M1M3Residual(nModes=nModes)
    m1m3rescomb = M1M3Residual(nModes=nModes)

    m1m3res.applyBending(up1)
    m1m3res.applyBending(up2)
    m1m3rescomb.applyBending(comb)

    np.testing.assert_allclose(m1m3res.surfResidual, m1m3rescomb.surfResidual)
