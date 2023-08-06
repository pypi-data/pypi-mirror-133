# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['bossICC', 'bossICC.Commands', 'bossICC.Controllers', 'bossICC.Simulators']

package_data = \
{'': ['*'], 'bossICC': ['etc/*', 'etc/CamProcedures/*']}

install_requires = \
['Twisted>=21.7.0,<22.0.0',
 'astropy>=4.3.1,<5.0.0',
 'click>=8.0.1,<9.0.0',
 'numpy>=1.21.1,<2.0.0',
 'sdss-actorcore>=5.0.4,<6.0.0',
 'sdsstools>=0.4.13']

entry_points = \
{'console_scripts': ['bossICC = bossICC.BossICC:run_actor']}

setup_kwargs = {
    'name': 'sdss-bossicc',
    'version': '6.0.1',
    'description': 'The BOSS Instrument Control Computer for APO.',
    'long_description': '# bossICC\n\nbossICC is the Instrument Control Computer for the BOSS spectrographs. It manages communications between other actors and the BOSS firmware, starting, stopping, and reading out exposures, moving collimators and other spectrograph mechanicals, and monitoring and managing voltages, pressures, and temperatures.\n\nConfiguration (e.g. hosts/ports/logging directories) are found in the `python/bossICC/etc/` directory. It should only be run on the `sdss5-boss-icc` virtual machine.\n\nThis product also can communicate with the engineering "benchboss" system by running `python python/bossICC/bossICC.py benchboss`.\n',
    'author': 'Craig Loomis',
    'author_email': None,
    'maintainer': 'José Sánchez-Gallego',
    'maintainer_email': 'gallegoj@uw.edu',
    'url': 'https://github.com/sdss/bossICC',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
