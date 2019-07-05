import numpy as np
from aos.metric import SumOfSquares


def test_sum_of_squares():
    x = np.arange(5)
    tm = SumOfSquares()
    assert tm.evaluate(x) == 30
