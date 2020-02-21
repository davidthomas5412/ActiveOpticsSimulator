import os
import yaml
import batoid
import numpy as np
from aos.mirror import M1M3Residual, M2Residual
from aos.state import BendingState, ZernikeState


class Telescope:
    """
    Class that wraps batoid optic for intra and extra-focal modes.

    Parameters
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.

    Attributes
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.
    """
    OFFSET = 1.5e-3

    def __init__(self, optic):
        self.optic = optic

    @property
    def intra(self):
        """
        Return optic with detector in intra-focal position.
        """
        return self.optic.withGloballyShiftedOptic('LSST.LSSTCamera.Detector',
                                                   [0, 0, -Telescope.OFFSET])

    @property
    def extra(self):
        """
        Return optic with detector in extra-focal position.
        """
        return self.optic.withGloballyShiftedOptic('LSST.LSSTCamera.Detector',
                                                   [0, 0, Telescope.OFFSET])

    @classmethod
    def nominal(cls, band='g'):
        """
        Provides the nominal LSST telescope.

        Parameters
        ----------
        band: str
            The LSST filter; default is 'g'.

        Returns
        -------
        ZernikeTelescope
            The nominal LSST telescope.
        """
        LSST_g_fn = os.path.join(batoid.datadir, "LSST", "LSST_{}.yaml".format(band))
        config = yaml.safe_load(open(LSST_g_fn))
        optic = batoid.parse.parse_optic(config['opticalSystem'])
        return cls(optic)

    def update(self, deltax):
        """
        Updates the optic.

        Parameters
        ----------
        deltax: aos.state.State
            The change in the optical state.

        Notes
        -----
        Rotations only commute for small angles; otherwise order matters.
        """
        camx, camy, camz, camrx, camry = deltax.camhex
        self.optic = self.optic.withGloballyShiftedOptic('LSST.LSSTCamera', [camx, camy, camz])
        camrot = np.dot(batoid.RotX(camrx), batoid.RotY(camry))
        self.optic = self.optic.withLocallyRotatedOptic('LSST.LSSTCamera', camrot)

        m2x, m2y, m2z, m2rx, m2ry = deltax.m2hex
        self.optic = self.optic.withGloballyShiftedOptic('LSST.M2', [m2x, m2y, m2z])
        m2rot = np.dot(batoid.RotX(m2rx), batoid.RotY(m2ry))
        self.optic = self.optic.withLocallyRotatedOptic('LSST.M2', m2rot)


class ZernikeTelescope(Telescope):
    """
    Class that wraps batoid optic, accumulates changes to the zernike state, and handles updates.

    Parameters
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.

    Attributes
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.
    """

    def __init__(self, optic):
        super().__init__(optic)

    def update(self, deltax):
        """
        Update the telescope based on the provided update to the optical state.

        Parameters
        ----------
        deltax: aos.state.ZernikeState
            The change in the optical state to apply to the telescope.
        """
        super().update(deltax)
        self.__updateSurface('LSST.M1', deltax.m1zer)
        self.__updateSurface('LSST.M2', deltax.m2zer)
        self.__updateSurface('LSST.M3', deltax.m3zer)

    def __updateSurface(self, name, zernikes):
        """
        Add zernike residual to mirror surface.

        Parameters
        ----------
        name: str
            The name of the mirror to update (ex. 'LSST_M1').
        zernikes: numpy.ndarray
            1D array with the zernike coefficients for the surface residual.
        """
        surf = self.optic.itemDict[name]
        residual = batoid.Zernike(zernikes, R_outer=surf.outRadius, R_inner=surf.inRadius)

        if isinstance(surf, batoid.Sum):
            nominal = surf.surfaces[0]
        else:
            nominal = surf.surface
        self.optic.itemDict[name].surface = batoid.Sum([nominal, residual])


class BendingTelescope(Telescope):
    """
    Class that wraps batoid optic, accumulates changes to the bending state, and handles updates.

    Parameters
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.
    m1m3Residual: aos.mirror.M1M3Residual
        The M1M3 residual surface; defaults to M1M3Residual with 5 modes.
    m2Residual: aos.mirror.M2Residual
        The M2 residual surface; defaults to M2Residual with 5 modes.

    Attributes
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.
    m1m3Residual: aos.mirror.M1M3Residual
        The M1M3 residual surface.
    m2Residual: aos.mirror.M2Residual
        The M2 residual surface.
    """

    def __init__(self, optic,
                 m1m3Residual=M1M3Residual(nModes=5),
                 m2Residual=M2Residual(nModes=5)):
        super().__init__(optic)
        self.m1m3res = m1m3Residual
        self.m2res = m2Residual

    def update(self, deltax):
        """
        Update the telescope based on the provided update to the optical state.

        Parameters
        ----------
        deltax: aos.state.BendingState
            The change in the optical state to apply to the telescope.
        """
        super().update(deltax)

        self.m1m3res.applyBending(deltax.m1m3modes)
        self.m2res.applyBending(deltax.m2modes)
        m1m3bicubic = batoid.Bicubic(self.m1m3res.x, self.m1m3res.y, self.m1m3res.surfResidual)
        m2bicubic = batoid.Bicubic(self.m2res.x, self.m2res.y, self.m2res.surfResidual)

        m1surf = self.optic.itemDict['LSST.M1']
        if isinstance(m1surf, batoid.Sum):
            m1nominal = m1surf.surfaces[0]
        else:
            m1nominal = m1surf.surface
        self.optic.itemDict['LSST.M1'].surface = batoid.Sum([m1nominal, m1m3bicubic])

        m3surf = self.optic.itemDict['LSST.M3']
        if isinstance(m1surf, batoid.Sum):
            m3nominal = m3surf.surfaces[0]
        else:
            m3nominal = m3surf.surface
        self.optic.itemDict['LSST.M3'].surface = batoid.Sum([m3nominal, m1m3bicubic])

        m2surf = self.optic.itemDict['LSST.M2']
        if isinstance(m1surf, batoid.Sum):
            m2nominal = m2surf.surfaces[0]
        else:
            m2nominal = m2surf.surface
        self.optic.itemDict['LSST.M2'].surface = batoid.Sum([m2nominal, m2bicubic])