from scipy.optimize import minimize
from aos.state import BendingState
from abc import ABC, abstractmethod


class Controller(ABC):
    """
    Abstract class for controllers that determine how to update the optical system.
    """
    @abstractmethod
    def nextState(self, x):
        """
        Parameters
        ----------
        x: numpy.ndarray
            Optical state.

        Returns
        -------
        numpy.ndarray, numpy.ndarray
            The next state and corresponding update.
        """
        pass


class GainController:
    """
    A controller that computes the next state by optimizing a metric and multiplying the
    optimal update by a gain.

    Parameters
    __________
    metric: aos.metric.Metric
        The metric to optimize for in the control loop.
    gain:
        Multiplicative gain for control loop; defaults to 1.

    Attributes
    ----------
    metric: aos.metric.Metric
        The metric to optimize for in the control loop.
    gain:
        Multiplicative gain for control loop; defaults to 1.
    """
    def __init__(self, metric, gain=1):
        self.metric = metric
        self.gain = gain

    def nextState(self, x):
        """
        Parameters
        ----------
        x: numpy.ndarray
            Optical state.

        Returns
        -------
        numpy.ndarray, numpy.ndarray
            The next state and corresponding update.
        """
        xprime = BendingState().state
        res = minimize(self.metric.evaluate, xprime)
        xdelta = (res.x - x) * self.gain
        xprime = x + xdelta
        return xprime, xdelta