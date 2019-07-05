import os
import aos
import numpy as np


class SurfaceResidual:
    """
    Class for representing and controlling mirror surface residuals.
    """
    def applyForce(self, force):
        # if len(force) != self.nActuators:
        #     raise ValueError('Force must have the same length as the number of actuators: {}'
        #                      .format(self.nActuators))
        # self.surfResidual += np.dot(self.influenceMatrix, force)
        # Note: reformat influence matrix to batoid grid
        raise NotImplementedError()

    def applyBending(self, deltaModes):
        """
        Updates surface residual based on bending modes.

        Parameters
        ----------
        modes: numpy.ndarray
            size of the bending modes, in meters.
        """
        if len(deltaModes) != self.nModes:
            raise ValueError('Modes must have the same length as the number of bending modes: {}'
                             .format(self.nModes))
        pert = self.bendingMatrix * deltaModes.reshape(self.nModes, 1, 1)
        self.surfResidual += np.sum(pert, axis=0)

    def applyThermal(self, temps):
        raise NotImplementedError()

    def applyGravity(self, zenith):
        raise NotImplementedError()


class M1M3Residual(SurfaceResidual):
    """
    M1M3 surface residuals.

    Parameters
    ----------
    modes: numpy.ndarray
        bending modes; defaults to None.

    forces: numpy.ndarray
        actuator forces; defaults to None.

    nModes: int
        number of modes to use; defaults to None.


    Attributes
    ----------
    x: numpy.ndarray
        The 1D 'x' axes grid points for the surface.
    y: numpy.ndarray
        The 1D 'y' axes grid points for the surface.
    bendingMatrix: numpy.ndarray
        The matrix that maps modes to the surface grid.
    nModes: int
        The number of bending modes to use.
    nActuators: int
        The number of actuators to use.
    surfResidual:
        The 2D grid of 'z' values corresponding to the grid of x,y.
    """
    def __init__(self, modes=None, forces=None, nModes=None):
        super().__init__()
        self.x = np.load(os.path.join(aos.dataDir, 'M1M3_grid_x.npy'))
        self.y = np.load(os.path.join(aos.dataDir, 'M1M3_grid_y.npy'))
        self.bendingMatrix = np.load(os.path.join(aos.dataDir, 'M1M3_bending_modes.npy'))
        if nModes is None:
            self.nModes = self.bendingMatrix.shape[0]
        else:
            self.bendingMatrix = self.bendingMatrix[:nModes]
            self.nModes = nModes

        self.nActuators = 256
        nx = len(self.x)
        ny = len(self.y)
        self.surfResidual = np.zeros((nx, ny))

        if modes is not None:
            self.setBending(modes)

        if forces is not None:
            self.applyForce(forces)


class M2Residual(SurfaceResidual):
    """
    M2 surface residuals.

    Parameters
    ----------
    modes: numpy.ndarray
        bending modes; defaults to None.

    forces: numpy.ndarray
        actuator forces; defaults to None.

    nModes: int
        number of modes to use; defaults to None.


    Attributes
    ----------
    x: numpy.ndarray
        The 1D 'x' axes grid points for the surface.
    y: numpy.ndarray
        The 1D 'y' axes grid points for the surface.
    bendingMatrix: numpy.ndarray
        The matrix that maps modes to the surface grid.
    nModes: int
        The number of bending modes to use.
    nActuators: int
        The number of actuators to use.
    surfResidual:
        The 2D grid of 'z' values corresponding to the grid of x,y.
    """
    def __init__(self, modes=None, forces=None, nModes=None):
        super().__init__()
        self.x = np.load(os.path.join(aos.dataDir, 'M2_grid_x.npy'))
        self.y = np.load(os.path.join(aos.dataDir, 'M2_grid_y.npy'))
        self.bendingMatrix = np.load(os.path.join(aos.dataDir, 'M2_bending_modes.npy'))
        if nModes is None:
            self.nModes = self.bendingMatrix.shape[0]
        else:
            self.bendingMatrix = self.bendingMatrix[:nModes]
            self.nModes = nModes
        self.nActuators = 256
        nx = len(self.x)
        ny = len(self.y)
        self.surfResidual = np.zeros((nx, ny))

        if modes is not None:
            self.setBending(modes)

        if forces is not None:
            self.applyForce(forces)