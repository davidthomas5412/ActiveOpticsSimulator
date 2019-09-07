import numpy as np
from abc import ABC, abstractmethod
from aos.state import State


class Metric(ABC):
    """
    A class to represent a metric of the optical state.
    Eventually will have non-trivial image quality metrics ...
    """
    @abstractmethod
    def evaluate(self, x):
        """
        Evaluates the metric on state x.

        Parameters
        ----------
        x : aos.state.State | numpy.ndarray[float]
            Optical state.
        """
        pass


class SumOfSquares(Metric):
    """
    A sum of squares metric.
    """

    def evaluate(self, x):
        """
        Computes the sum of squares of state x.

        Parameters
        ----------
        x : aos.state.State | numpy.ndarray[float]
            Optical state.

        Returns
        -------
        float
            Sum of squares.
        """
        if isinstance(x, State):
            x = x.array
        return np.sum(x ** 2)
