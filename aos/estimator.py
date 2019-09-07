import numpy as np
from galsim.zernike import zernikeBasis, Zernike


class WavefrontEstimator:
    """
    Class to estimate the wavefront zernike coefficients from wavefront images.

    Parameters
    ----------
    outRadius: float
        outer radius of entrance pupil in meters; defaults to 4.18 (LSST).
    inRadius: float
        inner radius of entrance pupil in meters; defaults to 2.558 (LSST).

    Attributes
    ----------
    outRadius: float
        outer radius of entrance pupil in meters; defaults to 4.18 (LSST).
    inRadius: float
        inner radius of entrance pupil in meters; defaults to 2.558 (LSST).
    """
    def __init__(self, outRadius=4.18, inRadius=2.558):
        self.outRadius = outRadius
        self.inRadius = inRadius

    def estimate(self, wavefront, nZern=22):
        """
        Fits zernikes to wavefront image.

        Notes
        -----
        The coefficients are indexed by the Noll (1976) convention, which starts at j=1. The 0th
        coefficient has no impact.

        Parameters
        ----------
        wavefront: numpy.ndarray
            wavefront image.

        nZern: int
            number of coefficients to fit.

        Returns
        -------
        numpy.ndarray
            the zernike coeficients (Noll .
        """
        nx = wavefront.shape[0]
        space = np.linspace(-self.outRadius, self.outRadius, nx)
        X, Y = np.meshgrid(space, space)
        mask = ~np.isnan(wavefront)
        basis = zernikeBasis(nZern, X[mask].flatten(), Y[mask].flatten(),
                             R_inner=self.inRadius, R_outer=self.outRadius)
        coefs, _, _, _ = np.linalg.lstsq(basis.T, wavefront[mask].flatten())
        return coefs

    def evaluate(self, coefs, nx=255):
        """
        Produce wavefront image from zernike coefficients.

        Notes
        -----
        The coefficients are indexed by the Noll (1976) convention, which starts at j=1. The 0th
        coefficient has no impact.

        Parameters
        ----------
        coefs: numpy.ndarray
            zernike coefficients.
        nx: int
            number of pixels in each dimension; defaults to 255.

        Returns
        -------
        numpy.ndarray
            image of wavefront.
        """
        space = np.linspace(-self.outRadius, self.outRadius, nx)
        X, Y = np.meshgrid(space, space)
        R = np.sqrt(X ** 2 + Y ** 2)
        mask = np.logical_and(R <= self.outRadius, R >= self.inRadius)
        zern = Zernike(coefs, R_inner=self.inRadius, R_outer=self.outRadius)
        img = zern.evalCartesian(X, Y)
        img[~mask] = np.nan
        return img


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