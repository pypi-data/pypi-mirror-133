# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['hartmannActor', 'hartmannActor.Commands']

package_data = \
{'': ['*'], 'hartmannActor': ['etc/*']}

install_requires = \
['astropy>=4.0,<5.0',
 'fitsio>=1.0.5,<2.0.0',
 'matplotlib>=3.1.2,<4.0.0',
 'numpy>=1.17.0',
 'scipy>=1.4.1,<2.0.0',
 'sdss-actorcore>=5.0.2,<6.0.0',
 'sdsstools>=0.4.10']

entry_points = \
{'console_scripts': ['hartmannActor = hartmannActor.hartmann:run_actor']}

setup_kwargs = {
    'name': 'sdss-hartmannactor',
    'version': '2.0.2',
    'description': 'An actor to analyse hartmann images and apply corrections.',
    'long_description': '# hartmannActor\n\n![Versions](https://img.shields.io/badge/python->=3.7-blue)\n[![Test](https://github.com/sdss/hartmannActor/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/hartmannActor/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/sdss/hartmannActor/branch/py3/graph/badge.svg)](https://codecov.io/gh/sdss/hartmannActor)\n\nThis commands the BOSS ICC to take Hartmann exposures, calculates the focus of the exposures, and if needed informs BOSS ICC to apply focus corrections to the collimator, and also the blue ring.\n',
    'author': 'John Parejko',
    'author_email': 'parejkoj@uw.edu',
    'maintainer': 'José Sánchez-Gallego',
    'maintainer_email': 'gallegoj@uw.edu',
    'url': 'https://github.com/sdss/hartmannActor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
