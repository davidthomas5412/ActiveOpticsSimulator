import os
import yaml
import batoid
import numpy as np
from aos.mirror import M1M3Residual, M2Residual
from aos.state import OpticalState


class Telescope:
    """
    Class that wraps batoid optic, accumulates changes to the state, and handles updates.

    Parameters
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.
    m1m3Residual: aos.mirror.M1M3Residual
        The M1M3 residual surface.
    m2Residual: aos.mirror.M2Residual
        The M2 residual surface.

    Attributes
    ----------
    optic: batoid.optic.CompoundOptic
        The optical system.
    m1m3Residual: aos.mirror.M1M3Residual
        The M1M3 residual surface.
    m2Residual: aos.mirror.M2Residual
        The M2 residual surface.
    """

    def __init__(self, optic, m1m3Residual, m2Residual):
        self.optic = optic
        self.m1m3res = m1m3Residual
        self.m2res = m2Residual

    def update(self, deltax):
        """
        Update the telescope based on the provided update to the optical state.

        Parameters
        ----------
        deltax: aos.state.OpticalState | numpy.ndarray
            The change in the optical state to apply to the telescope.
        """
        if not isinstance(deltax, OpticalState):
            deltax = OpticalState(deltax)
        camx, camy, camz, camrx, camry = deltax.camhex
        self.optic = self.optic.withGloballyShiftedOptic('LSST.LSSTCamera', [camx, camy, camz])
        # note: rotations only commute for small angles; otherwise order matters.
        camrot = np.dot(batoid.RotX(camrx), batoid.RotY(camry))
        self.optic = self.optic.withLocallyRotatedOptic('LSST.LSSTCamera', camrot)

        m2x, m2y, m2z, m2rx, m2ry = deltax.m2hex
        self.optic = self.optic.withGloballyShiftedOptic('LSST.M2', [m2x, m2y, m2z])
        # note: rotations only commute for small angles; otherwise order matters.
        m2rot = np.dot(batoid.RotX(m2rx), batoid.RotY(m2ry))
        self.optic = self.optic.withLocallyRotatedOptic('LSST.M2', m2rot)

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

    @staticmethod
    def nominal(band='g'):
        """
        Provides the nominal LSST telescope.

        Parameters
        ----------
        band: str
            The LSST filter; default is 'g'.

        Returns
        -------
        Telescope
            The nominal LSST telescope.
        """
        LSST_g_fn = os.path.join(batoid.datadir, "LSST", "LSST_{}.yaml".format(band))
        config = yaml.safe_load(open(LSST_g_fn))
        optic = batoid.parse.parse_optic(config['opticalSystem'])
        m1m3res = M1M3Residual(nModes=5)
        m2res = M2Residual(nModes=5)
        return Telescope(optic, m1m3res, m2res)