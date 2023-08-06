# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pickle_secure']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.0,<37.0.0']

setup_kwargs = {
    'name': 'pickle-secure',
    'version': '0.9.99',
    'description': 'Easily create encrypted pickle files',
    'long_description': '================================\npickle-secure: encrypted pickles\n================================\n\n.. image:: https://github.com/spapanik/pickle-secure/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/pickle-secure/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/pickle-secure.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/pickle-secure/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/pickle-secure\n  :alt: License\n  :target: https://github.com/spapanik/pickle-secure/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/pickle-secure\n  :alt: PyPI\n  :target: https://pypi.org/project/pickle-secure\n.. image:: https://pepy.tech/badge/pickle-secure\n  :alt: Downloads\n  :target: https://pepy.tech/project/pickle-secure\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``pickle-secure`` is a wrapper around pickle that creates encrypted pickles.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *pickle-secure* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    pickle-secure = "^0.9.0"\n\nUsage\n^^^^^\n\n``pickle-secure`` offers a similar API as the built-in pickle.\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/pickle-secure/blob/main/CHANGELOG.rst\n.. _Documentation: https://pickle-secure.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/pickle-secure',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
