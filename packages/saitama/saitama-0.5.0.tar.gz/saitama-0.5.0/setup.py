# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['saitama', 'saitama.queries']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2>=2.8.0,<3.0.0', 'tomlkit>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['punch = saitama.punch:main']}

setup_kwargs = {
    'name': 'saitama',
    'version': '0.5.0',
    'description': 'A python toolset to manage postgres migrations and testing',
    'long_description': '===================================\nsaitama: pure postgres unit-testing\n===================================\n\n.. image:: https://github.com/spapanik/saitama/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/saitama/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/saitama.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/saitama/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/saitama\n  :alt: License\n  :target: https://github.com/spapanik/saitama/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/saitama\n  :alt: PyPI\n  :target: https://pypi.org/project/saitama\n.. image:: https://pepy.tech/badge/saitama\n  :alt: Downloads\n  :target: https://pepy.tech/project/saitama\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``saitama`` is offering a way to write unittest and migrations in pure postgres.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use pip to install saitama.\n\n.. code:: console\n\n    $ pip install --user saitama\n\nUsage\n^^^^^\n\n``saitama``, once installed, offers a single command, ``punch``, that controls the migrations and the testing.\n``punch`` follows the GNU recommendations for command line interfaces, and offers:\n\n* ``-h`` or ``--help`` to print help, and\n* ``-V`` or ``--version`` to print the version\n\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/saitama/blob/main/CHANGELOG.rst\n.. _Documentation: https://saitama.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/saitama',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
