[![Build Status](https://travis-ci.com/davidthomas5412/ActiveOpticsSimulator.svg?branch=master)](https://travis-ci.com/davidthomas5412/ActiveOpticsSimulator)
[![codecov](https://codecov.io/gh/davidthomas5412/ActiveOpticsSimulator/branch/master/graph/badge.svg)](https://codecov.io/gh/davidthomas5412/ActiveOpticsSimulator)

# ActiveOpticsSimulator
A framework for simulating and researching the LSST Active Optics system. We hope to document and transfer much of the functionality in [bxin/IM](https://github.com/bxin/IM) (latest fork: [davidthomas5412/IM](https://github.com/davidthomas5412/IM)) and [bxin/cwfs](https://github.com/bxin/cwfs) (latest fork: [davidthomas5412/cwfs](https://github.com/davidthomas5412/cwfs)) into this new framework, as well as make it easy to explore alternative approaches. We will also be introducing the following software practices:

1. Testing: unit tests, continuous integration, track code coverage.
2. Documentation: numpy docstrings, no magic interpolations - all hardcoded matrices etc. must be derived or explained in corresponding notebooks.
3. Modular design: we strive to make it easy and natural for users to try new alternatives and swap 
out parts of the pipeline.
4. Switch simulators: zemax+phosim -> batoid+galsim.
5. Open source: public github repo, issue tracking, pull requests welcome.

# Install
This project has two dependencies that must be installed separately. First, you will need to install [galsim](https://github.com/GalSim-developers/GalSim). Then, you will need to install [batoid](https://github.com/jmeyers314/batoid). batoid must be installed from source because we depend on a functions (batoid.utils.fieldToDirCos and batoid.utils.dirCosToZemax) that have not made it into the PyPI release. Then you should be able to clone 
this repo and run setup.py:

```
git clone https://github.com/davidthomas5412/ActiveOpticsSimulator
cd ActiveOpticsSimulator
python setup.py install
```

# Tests

To run the unit tests, from the ActiveOpticsSimulator directory, first install the testing requirements:

```
pip install -r test_requirements.txt
```

And then run the tests using setup.py:

```
python setup.py test
```

# Getting Started with our Minimum Viable Product
We started off with a minimal viable product (MVP) that supports the following workflow:
1) create nominal telescope
2) create perturbed optical state and apply it to telescope
3) simulate OPD at the field center
4) estimate wavefront at field center from OPD image
5) use wavefront estimate to solve for optical correction by minimizing 
metric
6) apply new optical state to telescope
7) repeat

The snippet below runs two iterations of this primitive version of the active optics system:
```
from aos.simulator import OPDSimulator
from aos.estimator import OPDEstimator
from aos.metric import SumOfSquares
from aos.control import GainController
from aos.telescope import Telescope
from aos.state import OpticalState
from aos.solver import SensitivitySolver

telescope = Telescope.nominal(band='g')
simulator = OPDSimulator()
estimator = OPDEstimator()
solver = SensitivitySolver()
metric = SumOfSquares()
controller = GainController(metric, gain=0.3)
fieldx, fieldy = 0, 0

x = OpticalState()
# add 1 micron of the third bending mode to M2.
x['m2b3'] = 1e-6
telescope.update(x)
opd = simulator.simulate(telescope.optic, fieldx, fieldy)
yest = estimator.estimate(opd)
xest = solver.solve(yest)
xprime, xdelta = controller.nextState(xest)

# start second iteration
telescope.update(xdelta)
opd = simulator.simulate(telescope.optic, fieldx, fieldy)
yest = estimator.estimate(opd)
xest = solver.solve(yest)
xprime, xdelta = controller.nextState(xest)
```

There are a lot of degeneracies in the optical system at the field center, so the convergence is not great ... yet. 