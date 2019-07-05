import pytest
import numpy as np
from aos.solver import Solver, SensitivitySolver

def test_abstract_solver():
    with pytest.raises(TypeError):
        Solver()

def test_sensitivity_solver_nominal():
    solver = SensitivitySolver()
    y0 = solver.y0
    xest = solver.solve(y0)
    ref = np.zeros(20)

    np.testing.assert_allclose(xest, ref)
