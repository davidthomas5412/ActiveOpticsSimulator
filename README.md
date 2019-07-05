[![Build Status](https://travis-ci.com/davidthomas5412/ActiveOpticsSimulator.svg?branch=master)](https://travis-ci.com/davidthomas5412/ActiveOpticsSimulator)
[![codecov](https://codecov.io/gh/davidthomas5412/ActiveOpticsSimulator/branch/master/graph/badge.svg)](https://codecov.io/gh/davidthomas5412/ActiveOpticsSimulator)

# ActiveOpticsSimulator
A framework for simulating and researching the LSST Active Optics system. We hope to 
document and transfer much
 of the functionality in [bxin/IM](https://github.com/bxin/IM) (latest fork: [davidthomas5412/IM]
(https://github.com/davidthomas5412/IM)) and [bxin/cwfs](https://github.com/bxin/cwfs)(latest fork: 
[davidthomas5412/cwfs](https://github.com/davidthomas5412/cwfs)) into this new framework, as well
 as make it easy to explore alternative approaches. We will also be introducing the following 
 software practices:

1. Testing: unit tests, continuous integration, track code coverage.
2. Documentation: numpy docstrings, no magic interpolations - all hardcoded matrices etc. must be derived or explained in corresponding notebooks.
3. Modular design: we strive to make it easy and natural for users to try new alternatives and swap 
out parts of the pipeline.
4. Switch simulators: zemax+phosim -> batoid+galsim.
5. Open source: public github repo, issue tracking, pull requests welcome.

# Install
This project has two dependencies that must be installed separately.
First, you will need to install [galsim](https://github.com/GalSim-developers/GalSim). Then, you 
will need to install [batoid](https://github.com/jmeyers314/batoid). batoid must be installed 
from source because we depend on a functions (batoid.utils.fieldToDirCos and batoid.utils
.dirCosToZemax) that have not made it into the PyPI release. Then you should be able to clone 
this repo and run setup.py:

```
git clone https://github.com/davidthomas5412/ActiveOpticsSimulator
cd ActiveOpticsSimulator
python setup.py install
```

# Tests

To run the unit tests, from the ActiveOpticsSimulator directory, first install the testing
requirements:

```
pip install -r test_requirements.txt
```

And then run the tests using setup.py:

```
python setup.py test
```
