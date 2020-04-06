import numpy as np
from aos.survey import Survey

def test_survey_init():
    surv = Survey()
    assert np.all(surv.table['filter'] == 'r')