import numpy as np
from aos.state import BendingState, ZernikeState


def test_bending_state_dictionary():
    arr = np.arange(BendingState.LENGTH)
    state = BendingState(arr)

    assert state['camx'] == arr[0]

    state['m2b3'] = 1e-6

    assert state.array[17] == state['m2b3']


def test_zernike_state_dictionary():
    arr = np.arange(ZernikeState.LENGTH)
    state = ZernikeState(arr)

    assert state['m2rx'] == arr[8]

    state['m1zer4'] = 1e-6
    state['m2zer6'] = 2e-6
    state['m3zer15'] = 3e-6

    assert state.array[10] == state['m1zer4']
    assert state.array[24] == state['m2zer6']
    assert state.array[45] == state['m3zer15']



def test_bending_state_properties():
    arr = np.arange(BendingState.LENGTH)
    state = BendingState(arr)

    np.testing.assert_allclose(state.camhex, arr[:5])
    np.testing.assert_allclose(state.m2hex, arr[5:10])
    np.testing.assert_allclose(state.m1m3modes, arr[10:15])
    np.testing.assert_allclose(state.m2modes, arr[15:20])


def test_zernike_state_properties():
    arr = np.arange(ZernikeState.LENGTH)
    state = ZernikeState(arr)

    def zer(z4to16):
        z = np.zeros(16)
        z[4:] = z4to16
        return z

    np.testing.assert_allclose(state.camhex, arr[:5])
    np.testing.assert_allclose(state.m2hex, arr[5:10])
    np.testing.assert_allclose(state.m1zer, zer(arr[10:22]))
    np.testing.assert_allclose(state.m2zer, zer(arr[22:34]))
    np.testing.assert_allclose(state.m3zer, zer(arr[34:46]))
