import numpy as np
from aos.state import OpticalState


def test_state_dictionary():
    arr = np.arange(20)
    state = OpticalState(arr)

    assert state['camx'] == arr[0]

    state['m2b3'] = 1e-6

    assert state.state[17] == state['m2b3']


def test_state_properties():
    arr = np.arange(20)
    state = OpticalState(arr)

    np.testing.assert_allclose(state.camhex, arr[:5])
    np.testing.assert_allclose(state.m2hex, arr[5:10])
    np.testing.assert_allclose(state.m1m3modes, arr[10:15])
    np.testing.assert_allclose(state.m2modes, arr[15:20])
