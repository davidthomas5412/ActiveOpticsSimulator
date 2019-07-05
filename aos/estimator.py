import numpy as np
from galsim.zernike import zernikeBasis


class OPDEstimator:
    """
    Class to estimator the wavefront zernike coefficients from OPD images.

    Parameters
    ----------
    obscuration: float
        obscuration in optical system; defaults to 0.61 (LSST).
    nZern: int
        number of zernikes to use in the wavefront estimate; defaults to 22.

    Attributes
    ----------
    obscuration: float
        obscuration in optical system; defaults to 0.61 (LSST).
    nZern: int
        number of zernikes to use in the wavefront estimate; defaults to 22.
    """
    def __init__(self, obscuration=0.61, nZern=22):
        self.obscuration = 0.61
        self.nZern = nZern

    def estimate(self, opd):
        """
        Fits zernikes to opd image.

        Parameters
        ----------
        opd: batoid.Lattice
            opd image.

        Returns
        -------
        numpy.ndarray
            the zernike coeficients.
        """
        nx = opd.array.shape[0]
        X, Y = np.meshgrid(np.linspace(-1, 1, nx), np.linspace(-1, 1, nx))
        mask = ~opd.array.mask
        basis = zernikeBasis(self.nZern, X[mask].flatten(), Y[mask].flatten(),
                             R_inner=self.obscuration)
        coefs, _, _, _ = np.linalg.lstsq(basis.T, opd.array[mask].flatten())
        coefs = np.array(coefs[1:])
        return coefs


class InversionEstimator:
    """
    A class that will implement the inversion approach.
    """
    pass


class ForwardModelEstimator:
    """
    A class that will implement the forward model approach.
    """
    pass