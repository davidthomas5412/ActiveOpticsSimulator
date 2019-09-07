import numpy as np


class State(dict):
    """
    The telescope degrees of freedom.

    Notes
    -----
    Client can set optical state with the following syntax `state['camx'] = 1`.
    All degrees of freedom are in meters or radians depending on whether distance or angle.

    Parameters
    ----------
    array: numpy.ndarray
        A 1D array with the 10 degrees of freedom.

    Attributes
    ----------
    array: numpy.ndarray
        A 1D array with the 20 degrees of freedom.
    stateMap: dict(str, int)
        A dictionary mapping the name of the degree of freedom to its index in self.array.
    camhex: numpy.ndarray
        1D array with the 5 camera hexapod degrees of freedom.
    m2hex: numpy.ndarray
        1D array with the 5 camera hexapod degrees of freedom.
    """
    LENGTH = 10

    def __init__(self, array=None):
        self.array = np.zeros(State.LENGTH) if array is None else array
        self.stateMap = {
            'camx': 0,
            'camy': 1,
            'camz': 2,
            'camrx': 3,
            'camry': 4,
            'm2x': 5,
            'm2y': 6,
            'm2z': 7,
            'm2rx': 8,
            'm2ry': 9,
        }

    def __getitem__(self, key):
        ind = self.stateMap[key]
        return self.array[ind]

    def __setitem__(self, key, val):
        ind = self.stateMap[key]
        self.array[ind] = val

    @property
    def camhex(self):
        return self.array[:5]

    @property
    def m2hex(self):
        return self.array[5:10]


class BendingState(State):
    """
    The telescope degrees of freedom, with surfaces represented via bending modes.

    Parameters
    ----------
    array: numpy.ndarray
        A 1D array with the 20 degrees of freedom.

    Attributes
    ----------
    m1m3modes: numpy.ndarray
        1D array with the 5 M1M3 bending modes.
    m2modes: numpy.ndarray
        1D array with the 5 M2 bending modes.
    """
    LENGTH = 20

    def __init__(self, array=None):
        if array is None:
            array = np.zeros(BendingState.LENGTH)
        super().__init__(array)
        self.stateMap.update({
            'm1m3b1': 10,
            'm1m3b2': 11,
            'm1m3b3': 12,
            'm1m3b4': 13,
            'm1m3b5': 14,
            'm2b1': 15,
            'm2b2': 16,
            'm2b3': 17,
            'm2b4': 18,
            'm2b5': 19,
        })

    @property
    def m1m3modes(self):
        return self.array[10:15]

    @property
    def m2modes(self):
        return self.array[15:]


class ZernikeState(State):
    """
    The telescope degrees of freedom, with surfaces represented via zernike coefficients.

    Parameters
    ----------
    array: numpy.ndarray
        A 1D array with the 32 degrees of freedom.

    Attributes
    ----------
    m2z: numpy.ndarray
        1D array with the 18 M2 zernike coefficients (Z4-Z21).
    """
    LENGTH = 32

    def __init__(self, array=None):
        if array is None:
            array = np.zeros(ZernikeState.LENGTH)
        super().__init__(array)
        for i in range(22):
            self.stateMap['m2z{}'.format(i)] = i + 10

    @property
    def m2z(self):
        return self.array[10:]
