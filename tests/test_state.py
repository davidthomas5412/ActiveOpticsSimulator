import numpy as np
from aos.state import BendingState, ZernikeState


def test_bending_state_dictionary():
    arr = np.arange(20)
    state = BendingState(arr)

    assert state['camx'] == arr[0]

    state['m2b3'] = 1e-6

    assert state.state[17] == state['m2b3']


def test_zernike_state_dictionary():
    arr = np.arange(31)
    state = ZernikeState(arr)

    assert state['m2rx'] == arr[8]

    state['m2z17'] = 1e-6

    assert state.state[27] == state['m2z17']


def test_bending_state_properties():
    arr = np.arange(20)
    state = BendingState(arr)

    np.testing.assert_allclose(state.camhex, arr[:5])
    np.testing.assert_allclose(state.m2hex, arr[5:10])
    np.testing.assert_allclose(state.m1m3modes, arr[10:15])
    np.testing.assert_allclose(state.m2modes, arr[15:20])


def test_zernike_state_properties():
    arr = np.arange(31)
    state = ZernikeState(arr)

    np.testing.assert_allclose(state.camhex, arr[:5])
    np.testing.assert_allclose(state.m2hex, arr[5:10])
    np.testing.assert_allclose(state.m2z, arr[10:])
