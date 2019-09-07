import pytest
import numpy as np
from aos.solver import Solver, SensitivitySolver

def test_abstract_solver():
    with pytest.raises(TypeError):
        Solver()

def test_sensitivity_solver_nominal():
    solver = SensitivitySolver()
    y0 = np.zeros(len(solver.y0) + 1)
    # hack because Noll (1976) indexing starts from j=1
    y0[1:] = solver.y0
    xest = solver.solve(y0)
    ref = np.zeros(20)

    np.testing.assert_allclose(xest.array, ref)
