import numpy as np


class OpticalState(dict):
    """
    The optical degrees of freedom.

    Notes
    -----
    Client can set optical state with the following syntax `state['camx'] = 1`.
    All degrees of freedom are in meters or radians depending on whether distance or angle.

    Parameters
    ----------
    state: numpy.ndarray
        A 1D array with the 20 degrees of freedom.

    Attributes
    ----------
    state: numpy.ndarray
        A 1D array with the 20 degrees of freedom.
    stateMap: dict(str, int)
        A dictionary mapping the name of the degree of freedom to its index in the state array.
    camhex: numpy.ndarray
        1D array with the 5 camera hexapod degrees of freedom.
    m1m3modes: numpy.ndarray
        1D array with the 5 M1M3 bending modes.
    m2modes: numpy.ndarray
        1D array with the 5 M2 bending modes.
    """
    def __init__(self, state=None):
        self.state = np.zeros(20) if state is None else state
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
        }

    def __getitem__(self, key):
        ind = self.stateMap[key]
        return self.state[ind]

    def __setitem__(self, key, val):
        ind = self.stateMap[key]
        self.state[ind] = val

    @property
    def camhex(self):
        return self.state[:5]

    @property
    def m2hex(self):
        return self.state[5:10]

    @property
    def m1m3modes(self):
        return self.state[10:15]

    @property
    def m2modes(self):
        return self.state[15:]
