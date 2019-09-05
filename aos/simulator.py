import batoid
import numpy as np
from batoid.utils import fieldToDirCos


class OPDSimulator:
    """
    Simulates opd (optical path difference) images.

    Notes
    -----
    Start with grid on planar surface that intersects the perimeter of M1.
    Trace to exit pupil.
    Measure relative path differences with respect to the chief ray.

    Parameters
    ----------
    wavelength: float
        The wavelength of light to use.
    nx: int
        The grid size to use (grid = nx x nx pixels/rays).

    Attributes
    ----------
    wavelength: float
        The wavelength of light to use.
    nx: int
        The grid size to use (grid = nx x nx pixels/rays).
    """
    def __init__(self, wavelength=500e-9, nx=255):
        self.wavelength=wavelength
        self.nx=nx

    def simulate(self, optic, fieldx, fieldy):
        """
        Notes
        -----
        Thank you Josh Meyers for providing this snippet.

        Parameters
        ----------
        optic: batoid.optic.CompoundOptic
            The optical system to simulate.
        fieldx: float
            The x field position in radians.
        fieldy: float
            The y field position in radians.

        Returns
        -------
        batoid.Lattice
            The grid of relative path difference values.
        """
        theta_x, theta_y = np.deg2rad([fieldx, fieldy])
        dirCos = fieldToDirCos(theta_x, theta_y, projection='zemax')
        useLattice = (self.nx % 2 ==0)
        rays = batoid.rayGrid(
            optic.dist / dirCos[2], optic.pupilSize,
            dirCos[0], dirCos[1], -dirCos[2],
            self.nx, self.wavelength, 1.0, optic.inMedium,
            lattice=useLattice
        )

        # chief ray index.  works if lattice=True and nx is even,
        # or if lattice=False and nx is odd
        cridx = (self.nx // 2) * self.nx + self.nx // 2
        optic.traceInPlace(rays, outCoordSys=batoid.globalCoordSys)
        spherePoint = rays[cridx].r

        # We want to place the vertex of the reference sphere one radius length away from the
        # intersection point.  So transform our rays into that coordinate system.
        radius = np.hypot(optic.sphereRadius, np.hypot(spherePoint[0], spherePoint[1]))
        transform = batoid.CoordTransform(
            batoid.globalCoordSys, batoid.CoordSys(spherePoint + np.array([0, 0, radius])))
        transform.applyForwardInPlace(rays)

        sphere = batoid.Sphere(-radius)
        sphere.intersectInPlace(rays)
        t0 = rays[cridx].t
        arr = np.ma.masked_array((t0 - rays.t), mask=rays.vignetted)\
            .reshape(self.nx, self.nx)

        primitiveVectors = np.vstack([[optic.pupilSize / self.nx, 0],
                                      [0, optic.pupilSize / self.nx]])
        return batoid.Lattice(arr, primitiveVectors)


class DonutSimulator:
    """
    Simulates individual donut crops.

    Parameters
    ----------
    wavelength: float
        The wavelength of light to use.
    crop: int
        The number of pixels in donut crop.
    nphot: int
        The number of photons to use per donut.
    pix: float
        The size of a pixel in meters.

    Attributes
    ----------
    wavelength: float
        The wavelength of light to use.
    crop: int
        The number of pixels in donut crop.
    nphot: int
        The number of photons to use per donut.
    pix: float
        The size of a pixel in meters.

    Raises
    ------
    ValueError
        crop must be an even integer.
    """
    def __init__(self, wavelength=500e-9, crop=192, nphot=int(1e6), pix=10e-6):
        if crop % 2 == 1:
            raise ValueError('crop must be even integer.')

        self.wavelength = wavelength
        self.crop = crop
        self.nphot = nphot
        self.pix = pix

    def simulate(self, optic, fieldx, fieldy):
        """
        Simulate a donut image by raytracing photons through optic.

        Parameters
        ----------
        optic: batoid.Optic
            The optic to raytrace through.
        fieldx: float
            The x field position in radians.
        theta_y: float
            The y field position in radians.

        Returns
        -------
        batoid.Lattice
            The donut image.
        """
        flux = 1
        xcos, ycos, zcos = batoid.utils.gnomonicToDirCos(fieldx, fieldy)
        rays = batoid.uniformCircularGrid(
            optic.dist,
            optic.pupilSize / 2,
            optic.pupilSize * optic.pupilObscuration / 2,
            xcos, ycos, -zcos,
            self.nphot, self.wavelength, flux,
            optic.inMedium)
        optic.traceInPlace(rays)
        rays.trimVignettedInPlace()

        xcent, ycent = np.mean(rays.x), np.mean(rays.y)
        width = self.crop * self.pix

        xedges = np.arange(xcent - width / 2, xcent + width / 2, self.pix)
        yedges = np.arange(ycent - width / 2, ycent + width / 2, self.pix)

        # flip here because 1st dimension corresponds to y-dimension in bitmap image
        result, _, _ = np.histogram2d(rays.y, rays.x, bins=[yedges, xedges])

        primitiveX = np.array([[self.pix, 0], [0, self.pix]])
        return batoid.Lattice(result, primitiveX)


class StarSimulator:
    """
    Simulator for realistic LSST images.
    """
    def simulateCatalog(self, observation, telescope, catalog):
        raise NotImplementedError()