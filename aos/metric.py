import numpy as np
from abc import ABC, abstractmethod


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
        x : numpy.ndarray
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
        x : numpy.ndarray
            Optical state.

        Returns
        -------
        float
            Sum of squares.
        """
        return np.sum(x ** 2)
