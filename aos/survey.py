import os
from aos import dataDir
from astropy.table import Table

class Survey:
    """
    Stores table of LSST observations.

    Parameters
    ----------
    table: astropy.table.Table
        The LSST observations.

    Notes
    -----
    The raw data is generated from the OpSim baseline_2snapsv1.4_10yrs.db database. The query is:

    SELECT observationId, fieldRA, fieldDec, filter, rotTelPos, altitude, skyBrightness, seeingFwhm500 
    FROM SummaryAllProps WHERE filter IS "r" ORDER BY random() LIMIT 50;

    """
    survey_file = 'survey.csv'

    def __init__(self):
        self.table = Table.read(os.path.join(dataDir, Survey.survey_file),
                        names=['observationId', 'fieldRA', 'fieldDec', 'filter', 'rotTelPos', 'altitude', 'skyBrightness', 'seeingFwhm500'])