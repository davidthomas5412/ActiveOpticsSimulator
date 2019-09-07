import numpy as np
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
        x: aos.state.State
            Optical state.

        Returns
        -------
        aos.state.State, aos.state.State
            The next state and corresponding update.
        """
        pass


class GainController(Controller):
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
        x: aos.state.State
            Optical state.

        Returns
        -------
        aos.state.BendingState, aos.state.BendingState
            The next state and corresponding update.
        """
        xprime = np.zeros(BendingState.LENGTH)
        res = minimize(self.metric.evaluate, xprime)
        xdelta = BendingState((res.x - x.array) * self.gain)
        xprime = BendingState(x.array + xdelta.array)
        return xprime, xdelta
