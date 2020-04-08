import os
import numpy as np
from aos import dataDir
from aos.constant import h,c,k,b

class Bandpass:
    """
    Computes wavelength dependent bandpass function for atmosphere and LSST.

    Parameters
    ----------
    wavelengths: numpy.ndarray
        The wavelengths of the bandpass curve (in m).
    bandpass: numpy.ndarray
        The bandpass efficiency of the corresponding wavelengths.
    low: int
        The lowest wavelength (in m).
    high: int
        The highest wavelength (in m).
    """
    def __init__(self, wavelengths, bandpass):
        self.wavelengths = wavelengths.astype('int') * 1e-9
        self.bandpass = bandpass
        self.low = np.min(self.wavelengths)
        self.high = np.max(self.wavelengths)

    @staticmethod
    def u():
        """
        Returns
        -------
        Bandpass
            The LSST u-band bandpass function.
        """
        data = np.load(os.path.join(dataDir, 'total_u.npy'))
        return Bandpass(data[:,0], data[:,1])

    @staticmethod
    def g():
        """
        Returns
        -------
        Bandpass
            The LSST g-band bandpass function.
        """
        data = np.load(os.path.join(dataDir, 'total_g.npy'))
        return Bandpass(data[:,0], data[:,1])

    @staticmethod
    def r():
        """
        Returns
        -------
        Bandpass
            The LSST r-band bandpass function.
        """
        data = np.load(os.path.join(dataDir, 'total_r.npy'))
        return Bandpass(data[:,0], data[:,1])
    
    @staticmethod
    def i():
        """
        Returns
        -------
        Bandpass
            The LSST i-band bandpass function.
        """
        data = np.load(os.path.join(dataDir, 'total_i.npy'))
        return Bandpass(data[:,0], data[:,1])

    @staticmethod
    def z():
        """
        Returns
        -------
        Bandpass
            The LSST z-band bandpass function.
        """
        data = np.load(os.path.join(dataDir, 'total_z.npy'))
        return Bandpass(data[:,0], data[:,1])

    @staticmethod
    def y():
        """
        Returns
        -------
        Bandpass
            The LSST y-band bandpass function.
        """
        data = np.load(os.path.join(dataDir, 'total_y.npy'))
        return Bandpass(data[:,0], data[:,1])

class SED:
    """
    Spectral energy distribution base class.
    """
    def spectrum(self):
        raise NotImplementedError()

    def sample(self, size):
        raise NotImplementedError()

class Monochromatic(SED):
    """
    Monochromatic spectral energy distribution.

    Parameters
    ----------
    wavelength: float
        Central wavelength.
    wavelengths: numpy.ndarray
        Wavelengths centered on the central wavelength.
    spec: numpy.ndarray
        The spectrum, in this case all zeros except a one at the index of the central wavelength.
    """
    def __init__(self, wavelength=500e-9):
        super().__init__()
        self.wavelength = wavelength
        self.wavelengths = np.array([wavelength - 1e-9, wavelength, wavelength + 1e-9])
        self.spec = np.array([0,1,0])

    def spectrum(self):
        """
        Returns
        -------
        numpy.ndarray, numpy.ndarray
            The probability distribution as a function of wavelength.
        """
        return self.wavelengths, self.spec
    
    def sample(self, nphot):
        """
        Parameters
        ----------
        nphot: int | float
            The number of wavelengths to sample.

        Returns
        -------
        numpy.ndarray
            Samples nphot wavelengths from this distribution.
        """
        return np.ones(int(nphot)) * self.wavelength

class Blackbody(SED):
    """
    Blackbody spectral energy distribution from Planck's law that can be combined with bandpass function and sampled. 

    Parameters
    ----------
    temperature: float
        The temperature of the blackbody. Default is None; overrides wavelength through Wien's law if provided.
    wavelength: float
        The central wavelength of the blackbody spectrum.
    bandpass: Bandpass
        The throughput of the system (atmosphere, optics, detector).

    TODO: add attributes.
    """

    def __init__(self, temperature=None, wavelength=500e-9, bandpass=Bandpass.g()):
        super().__init__()
        if temperature is not None:
            wavelength = b / temperature
        self.bandpass = bandpass
        self.wavelength = wavelength
        T = b / wavelength
        self.wavelengths = self.bandpass.wavelengths
        self.spec = 2 * h * c ** 2 * self.wavelengths ** -5 * (np.exp(h * c / (self.wavelengths * k * T)) - 1) ** -1
        self.spec /= np.sum(self.spec)
        self.bp_spec = self.spec * self.bandpass.bandpass
        self.bp_factor = np.sum(self.bp_spec)
        self.bp_cdf = np.cumsum(self.bp_spec) / self.bp_factor

    def spectrum(self):
        """
        Returns
        -------
        numpy.ndarray, numpy.ndarray
            The probability distribution as a function of wavelength.
        """
        return self.wavelengths, self.bp_spec / self.bp_factor
    
    def sample(self, nphot):
        """
        Parameters
        ----------
        nphot: int | float
            The number of wavelengths to sample.

        Returns
        -------
        numpy.ndarray
            Samples nphot wavelengths from this distribution.
        """
        size = int(nphot * self.bp_factor)
        ind = np.searchsorted(self.bp_cdf, np.random.uniform(0, 1, size=size))
        return self.wavelengths[[ind]]