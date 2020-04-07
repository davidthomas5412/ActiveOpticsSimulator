import os
from numpy.testing import assert_raises
from aos.catalog import GaiaCatalog
from aos.focal_plane import WavefrontSensors

def test_gaia_launch_query():
    ws = WavefrontSensors()
    with open('test.csv_intra', 'w') as w:
        w.write("""source_id,ra,dec,teff_val,phot_g_mean_mag,phot_bp_mean_mag,phot_rp_mean_mag,focal
2449585742022146176,1.0764272684987302,-1.207319846371923,3000,13.5,14,14.1,intra""")
    with open('test.csv_extra', 'w') as w:
        w.write("""source_id,ra,dec,teff_val,phot_g_mean_mag,phot_bp_mean_mag,phot_rp_mean_mag,focal
2449587528728559616,1.2728371460657626,-1.116441304442664,3400,14.6,15,14.5,extra""")
    GaiaCatalog.launch_query(ws, 'test.csv', test=True)
    assert True

def test_gaia_catalog():
    gc = GaiaCatalog()
    for c in {'source_id', 'ra', 'dec', 'teff_val', 'phot_g_mean_mag', 'phot_bp_mean_mag', 'phot_rp_mean_mag', 'focal', 'lsst_r_mag'}:
        assert c in gc.table.columns