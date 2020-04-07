"""
This script generates the gaia catalogs.
"""
from time import time
from aos.survey import Survey
from aos.focal_plane import WavefrontSensors
from aos.catalog import GaiaCatalog

for obs, ra, dec in Survey().table['observationId', 'fieldRA', 'fieldDec']:
    print(time())
    ws = WavefrontSensors(ra, dec)
    GaiaCatalog.launch_query(ws, f'gaia_catalog_{obs}.csv', mag_cutoff=25, verbose=False)