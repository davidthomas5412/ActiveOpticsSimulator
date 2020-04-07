import os
from aos import catDir
from aos.constant import h,c
from astropy.table import Table, vstack
from astroquery.gaia import Gaia

class GaiaCatalog:
    """
    Class for gaia catalog tables.

    Parameters
    ----------
    table: astropy.table.Table
        The catalog.
    """
    def __init__(self, observation=19436):
        self.table = Table.read(os.path.join(catDir, f'gaia_catalog_{observation}.csv'))

    @staticmethod
    def __make_query(mag_cutoff, chips):
        """
        Forms Gaia Archive ADQL query.

        Parameters
        ----------
        mag_cutoff: aos.state.State
            Optical state.
        
        chips: list[aos.focal_plane.Chip]
            List of either intra or extra-focal chips.

        Returns
        -------
        string
            Gaia Archive ADQL query.
        """
        return f"""SELECT source_id, ra, dec, teff_val, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag FROM gaiadr2.gaia_source
        WHERE phot_g_mean_mag < {mag_cutoff}
        AND (1=CONTAINS(POINT('ICRS',ra,dec), {chips[0].polygon_string()}) 
        OR 1=CONTAINS(POINT('ICRS',ra,dec), {chips[1].polygon_string()}) 
        OR 1=CONTAINS(POINT('ICRS',ra,dec), {chips[2].polygon_string()}) 
        OR 1=CONTAINS(POINT('ICRS',ra,dec), {chips[3].polygon_string()}))
        """

    @staticmethod
    def launch_query(wavefront_sensors, output_path, mag_cutoff=25, test=False, verbose=True):
        """
        Launches Gaia Archive Queries and augments the results.

        Parameters
        ----------
        wavefront_sensors: aos.focal_plane.WavefrontSensors
            Sensors used to restrict query region.
        output_path: string
            The path to write table/catalog to.
        mag_cutoff: float | int
            Ignore sources fainter than this cutoff.
        test: bool
            Whether to run in test mode.
        verbose:
            Whether to launch query with verbose flag.

        Notes
        -----
        The lsst_r_mag relationship comes from 
        https://gea.esac.esa.int/archive/documentation/GDR2/Data_processing/chap_cu5pho/sec_cu5pho_calibr/ssec_cu5pho_PhotTransf.html
        viewed on 2020/4/7.
        """
        intras = wavefront_sensors.intras
        intra_query = GaiaCatalog.__make_query(mag_cutoff, wavefront_sensors.intras)
        # temporary intermediate path
        intra_path = output_path + '_intra'

        extras = wavefront_sensors.extras
        extra_query = GaiaCatalog.__make_query(mag_cutoff, wavefront_sensors.extras)
        # temporary intermediate path
        extra_path = output_path + '_extra'

        if not test:
            Gaia.launch_job_async(query=intra_query, output_file=intra_path, output_format='csv', verbose=verbose, dump_to_file=True, background=False)
            Gaia.launch_job_async(query=extra_query, output_file=extra_path, output_format='csv', verbose=verbose, dump_to_file=True, background=False)

        intra = Table.read(intra_path, format='csv')
        extra = Table.read(extra_path, format='csv')
        intra['focal'] = 'intra'
        extra['focal'] = 'extra'
        out = vstack([intra, extra])

        # convert magnitudes
        x = out['phot_bp_mean_mag'] - out['phot_rp_mean_mag']
        G_minus_r = -0.12879 + 0.24662 * x - 0.027464 * x ** 2 - 0.049465 * x ** 3
        out['lsst_r_mag'] = out['phot_g_mean_mag'] - G_minus_r

        if not test:
            out.write(output_path, overwrite=True)

        # delete temporary files
        os.remove(intra_path)
        os.remove(extra_path)