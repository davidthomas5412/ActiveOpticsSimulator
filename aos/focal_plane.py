import os
import pickle
import numpy as np
from aos import dataDir

class WavefrontSensors:
    """
    Manages boundaries of wavefront sensors.

    Parameters
    ----------
    ra: int | float
        Right ascension of telescope pointing; defaults to 0.
    dec: int | float
        Declination of telescope pointing; defaults to 0.
    
    Attributes
    ----------
    ra: int | float
        Right ascension of telescope pointing.
    dec: int | float
        Declination of telescope pointing.
    chips: dict[string] -> aos.focal_plane.Chip
        The 8 wavefront sensor chips (name -> chip).
    intras: list[aos.focal_plane.Chip]
        The 4 intra-focal chips.
    extras: list[aos.focal_plane.Chip]
        The 4 extra-focal chips.
    """
    path = os.path.join(dataDir, 'wavefront_sensor_corners.pickle')

    def __init__(self, ra=0, dec=0):
        self.ra = ra
        self.dec = dec
        self.chips = dict()
        with open(WavefrontSensors.path, 'rb') as r:
            pick = pickle.load(r)
        for k,v in pick.items():
            corners = np.rad2deg(np.array([[v['x'][0], v['y'][0]], 
                                [v['x'][0], v['y'][1]], 
                                [v['x'][1], v['y'][1]], 
                                [v['x'][1], v['y'][0]]]))
            corners[:,0] += ra
            corners[:,1] += dec

            chip = Chip(k, corners, v['focal'])
            self.chips[k] = chip
        
        self.intras = [self.chips[k] for k in ['R:0,0 S:2,2,A', 'R:0,4 S:2,0,A', 'R:4,0 S:0,2,A', 'R:4,4 S:0,0,A']]
        self.extras = [self.chips[k] for k in ['R:0,0 S:2,2,B', 'R:0,4 S:2,0,B', 'R:4,0 S:0,2,B', 'R:4,4 S:0,0,B']]

class Chip:
    """
    A single wavefront sensor chip.

    Parameters
    ----------
    name: string
        Canonical chip name.
    corners: numpy.ndarray
        The 4 corners of the chip.
    focal: string
        Whether the chip is intra or extra-focal.

    Raises
    ------
    ValueError
        If the shape of corners is not (4,2) or focal is not 'intra' or 'extra'.
    
    Attributes
    ----------
    name: string
        Canonical chip name.
    corners: numpy.ndarray
        The 4 corners of the chip.
    focal: string
        Whether the chip is intra or extra-focal.
    """
    def __init__(self, name, corners, focal):
        if corners.shape != (4,2):
            raise ValueError('corners must be (4,2)')
        elif focal not in {'intra', 'extra'}:
            raise ValueError('focal must be intra | extra')

        self.name = name
        self.corners = corners
        self.focal = focal

    def polygon_string(self):
        """
        Returns
        -------
        string
            The ADQL query for the region spanned by this chip.
        """
        return f"POLYGON('ICRS', {self.corners[0,0]}, {self.corners[0,1]},{self.corners[1,0]}, {self.corners[1,1]},{self.corners[2,0]}, {self.corners[2,1]},{self.corners[3,0]}, {self.corners[3,1]})"