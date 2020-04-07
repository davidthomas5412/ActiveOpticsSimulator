from setuptools import setup

setup(
    name='aos',
    version='0.2',
    author='David Thomas',
    author_email='davidthomas5412@gmail.com',
    url='https://github.com/davidthomas5412/ActiveOpticsSimulator',
    description="A Simulator for LSST Active Optics System",
    packages = ['aos'],
    package_data = {'aos': ['../data/*', '../data/catalogs/*', '../tests/*']},
    install_requires=['numpy', 'scipy', 'pyyaml', 'astropy', 'astroquery'],
    python_requires='>=3.4',
    tests_require=['pytest', 'pytest-cov', 'coverage', 'codecov']
)