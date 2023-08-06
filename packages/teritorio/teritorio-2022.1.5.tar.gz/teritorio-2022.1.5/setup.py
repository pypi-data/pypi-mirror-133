# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['teritorio']

package_data = \
{'': ['*'], 'teritorio': ['_data/*']}

setup_kwargs = {
    'name': 'teritorio',
    'version': '2022.1.5',
    'description': 'A library for country and currency ISO codes',
    'long_description': '=================================================\nteritorio: ISO codes for countries and currencies\n=================================================\n\n.. image:: https://github.com/spapanik/teritorio/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/teritorio/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/teritorio.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/teritorio/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/teritorio\n  :alt: License\n  :target: https://github.com/spapanik/teritorio/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/teritorio\n  :alt: PyPI\n  :target: https://pypi.org/project/teritorio\n.. image:: https://pepy.tech/badge/teritorio\n  :alt: Downloads\n  :target: https://pepy.tech/project/teritorio\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``teritorio`` two iterable singletons that ``Countries`` and ``Currencies``, that contain all the\nrelevant ISO information about countries and currencies, respectively.\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *teritorio* to them.\nIt requires Python 3.7.0+ to run.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    teritorio = "*"\n\nIt is advised to always use the latest release, so that you\'ll get the latest ISO codes\n\nUsage\n^^^^^\n\nThere are two iterable singletons that can be imported from ``teritorio``: ``Countries`` and ``Currencies``.\n\n.. code:: python\n\n    from teritorio import Countries\n    from teritorio import Currencies\n\nVersioning\n----------\n\nThe project project adheres to `Calendar Versioning`_.\nThe reason is that the data are dominated by political decisions,\nmaking semantic versioning largely irrelevant.\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _Calendar Versioning: https://calver.org\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/teritorio/blob/main/CHANGELOG.rst\n.. _Documentation: https://teritorio.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/teritorio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
