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

    state['m1m3zer4'] = 1e-6
    state['m2zer6'] = 2e-6

    assert state.array[10] == state['m1m3zer4']
    assert state.array[30] == state['m2zer6']



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

    def zer(z4to22):
        z = np.zeros(22)
        z[4:] = z4to22
        return z

    np.testing.assert_allclose(state.camhex, arr[:5])
    np.testing.assert_allclose(state.m2hex, arr[5:10])
    np.testing.assert_allclose(state.m1m3zer, zer(arr[10:28]))
    np.testing.assert_allclose(state.m2zer, zer(arr[28:46]))
