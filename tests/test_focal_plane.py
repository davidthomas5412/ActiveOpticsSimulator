import numpy as np
from numpy.testing import assert_raises, assert_allclose
from aos.focal_plane import Chip, WavefrontSensors

def test_chip():
    valid_array = np.array([[1,1],[1,1],[1,1],[1,1]])
    invalid_array = np.array([[1,1],[1,1],[1,1]])

    Chip('name', valid_array, 'intra')
    
    with assert_raises(ValueError):
        # wrong dimensions
        Chip('name', invalid_array, 'intra')
    
    with assert_raises(ValueError):
        # space after intra
        Chip('name', valid_array, 'intra ')

def test_wavefront_sensors():
    ws = WavefrontSensors()
    assert len(ws.intras) == 4
    assert len(ws.extras) == 4

    assert ws.intras[0].focal == 'intra'
    assert ws.extras[0].focal == 'extra'

def test_wavefront_translation():
    ws1 = WavefrontSensors()
    ws2 = WavefrontSensors(ra=1,dec=2)
    
    assert ws2.ra == 1
    assert ws2.dec == 2

    for i in range(4):
        assert_allclose(ws1.intras[i].corners[:,0], ws2.intras[i].corners[:,0] - ws2.ra)
        assert_allclose(ws1.intras[i].corners[:,1], ws2.intras[i].corners[:,1] - ws2.dec)
        assert_allclose(ws1.extras[i].corners[:,0], ws2.extras[i].corners[:,0] - ws2.ra)
        assert_allclose(ws1.extras[i].corners[:,1], ws2.extras[i].corners[:,1] - ws2.dec)