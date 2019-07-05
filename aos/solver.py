import numpy as np
from aos.state import OpticalState
from abc import ABC, abstractmethod


class Solver(ABC):
    """
    Abstract class for solving for the optical state.
    """
    @abstractmethod
    def solve(self, y):
        """
        Solves for the optical state.

        Parameters
        ----------
        y: numpy.ndarray
            The wavefront

        Returns
        -------
        numpy.ndarray
            The optical state that produces wavefront y.
        """
        pass


class SensitivitySolver(Solver):
    """
    Solves for optical state with a sensitivity matrix.

    Parameters
    ----------
    field: (float, float)
        Field position of the wavefront.

    Attributes
    ----------
    A: numpy.ndarray
        The sensitivity matrix mapping the optical state to the wavefront.
    Ainv: numpy.ndarray
        The psuedoinverse of the sensitivity matrix.
    y0: numpy.ndarray
        The wavefront from the nominal optical system.
    """
    def __init__(self, field=(0,0)):
        if not (field[0] == 0  and field[1] == 0):
            raise NotImplementedError()
        self.A = np.load('../data/sensitivity_matrix_20dof.npy')
        self.Ainv = np.linalg.pinv(self.A, rcond=1e-4)
        self.y0 = np.load('../data/nominal_wavefront_20dof.npy')

    def solve(self, y):
        """
        Solves for the optical state.

        Notes
        -----
        Math: x = psuedoInverse(A) (y-y0)

        Parameters
        ----------
        y: numpy.ndarray
            The wavefront

        Returns
        -------
        numpy.ndarray
            The optical state that produces wavefront y.
        """
        xest = np.dot(self.Ainv, (y - self.y0))
        return xest