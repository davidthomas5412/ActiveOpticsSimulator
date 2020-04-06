import os
import numpy as np
from aos import dataDir
from aos.constant import h,c,k,b

class Transmission:
    """
    Computes wavelength dependent transmission function for atmosphere and LSST.

    Parameters
    ----------
    wavelengths: numpy.ndarray
        The wavelengths of the transmission curve (in m).
    transmission: numpy.ndarray
        The transmission efficiency of the corresponding wavelengths.
    low: int
        The lowest wavelength (in m).
    high: int
        The highest wavelength (in m).
    """
    def __init__(self, wavelengths, transmission):
        self.wavelengths = wavelengths.astype('int') * 1e-9
        self.transmission = transmission
        self.low = np.min(self.wavelengths)
        self.high = np.max(self.wavelengths)

    @staticmethod
    def u():
        """
        Returns
        -------
        Transmission
            The LSST u-band transmission function.
        """
        data = np.load(os.path.join(dataDir, 'total_u.npy'))
        return Transmission(data[:,0], data[:,1])

    @staticmethod
    def g():
        """
        Returns
        -------
        Transmission
            The LSST g-band transmission function.
        """
        data = np.load(os.path.join(dataDir, 'total_g.npy'))
        return Transmission(data[:,0], data[:,1])

    @staticmethod
    def r():
        """
        Returns
        -------
        Transmission
            The LSST r-band transmission function.
        """
        data = np.load(os.path.join(dataDir, 'total_r.npy'))
        return Transmission(data[:,0], data[:,1])
    
    @staticmethod
    def i():
        """
        Returns
        -------
        Transmission
            The LSST i-band transmission function.
        """
        data = np.load(os.path.join(dataDir, 'total_i.npy'))
        return Transmission(data[:,0], data[:,1])

    @staticmethod
    def z():
        """
        Returns
        -------
        Transmission
            The LSST z-band transmission function.
        """
        data = np.load(os.path.join(dataDir, 'total_z.npy'))
        return Transmission(data[:,0], data[:,1])

    @staticmethod
    def y():
        """
        Returns
        -------
        Transmission
            The LSST y-band transmission function.
        """
        data = np.load(os.path.join(dataDir, 'total_y.npy'))
        return Transmission(data[:,0], data[:,1])

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
    Blackbody spectral energy distribution from Planck's law that can be combined with transmission function and sampled. 

    Parameters
    ----------
    temperature: float
        The temperature of the blackbody. Default is None; overrides wavelength through Wien's law if provided.
    wavelength: float
        The central wavelength of the blackbody spectrum.
    transmission: Transmission
        The throughput of the system (atmosphere, optics, detector).

    TODO: add attributes.
    """

    def __init__(self, temperature=None, wavelength=500e-9, transmission=Transmission.g()):
        super().__init__()
        if temperature is not None:
            wavelength = b / temperature
        self.transmission = transmission
        self.wavelength = wavelength
        T = b / wavelength
        self.wavelengths = self.transmission.wavelengths
        self.spec = 2 * h * c ** 2 * self.wavelengths ** -5 * (np.exp(h * c / (self.wavelengths * k * T)) - 1) ** -1
        self.spec /= np.sum(self.spec)
        self.trans_spec = self.spec * self.transmission.transmission
        self.trans_factor = np.sum(self.trans_spec)
        self.trans_cdf = np.cumsum(self.trans_spec) / self.trans_factor

    def spectrum(self):
        """
        Returns
        -------
        numpy.ndarray, numpy.ndarray
            The probability distribution as a function of wavelength.
        """
        return self.wavelengths, self.trans_spec / self.trans_factor
    
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
        size = int(nphot * self.trans_factor)
        ind = np.searchsorted(self.trans_cdf, np.random.uniform(0, 1, size=size))
        return self.wavelengths[[ind]]