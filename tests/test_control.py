import numpy as np
import pytest
from aos.metric import SumOfSquares
from aos.control import Controller, GainController


def test_abstract_controller():
    with pytest.raises(TypeError):
        Controller()


def test_gain_controller():
    x = np.arange(20)
    sos = SumOfSquares()
    controller = GainController(sos)
    xprime, xdelta = controller.nextState(x)

    np.testing.assert_array_almost_equal(xprime, 0)
    np.testing.assert_array_almost_equal(xdelta, -x)

    gain = 0.3
    controller = GainController(sos, gain=gain)
    xprime, xdelta = controller.nextState(x)

    np.testing.assert_array_almost_equal(xprime, x * (1 - gain))
    np.testing.assert_array_almost_equal(xdelta, -x * gain)
