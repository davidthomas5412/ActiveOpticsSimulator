import numpy as np
from aos.metric import SumOfSquares
from aos.state import BendingState


def test_sum_of_squares():
    arr = np.arange(BendingState.LENGTH)
    x = BendingState(arr)
    tm = SumOfSquares()
    ref = np.sum(np.arange(BendingState.LENGTH) ** 2)
    assert tm.evaluate(x) == ref
