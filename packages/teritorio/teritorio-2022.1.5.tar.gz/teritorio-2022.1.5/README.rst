=================================================
teritorio: ISO codes for countries and currencies
=================================================

.. image:: https://github.com/spapanik/teritorio/actions/workflows/build.yml/badge.svg
  :alt: Build
  :target: https://github.com/spapanik/teritorio/actions/workflows/build.yml
.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/teritorio.svg
  :alt: Total alerts
  :target: https://lgtm.com/projects/g/spapanik/teritorio/alerts/
.. image:: https://img.shields.io/github/license/spapanik/teritorio
  :alt: License
  :target: https://github.com/spapanik/teritorio/blob/main/LICENSE.txt
.. image:: https://img.shields.io/pypi/v/teritorio
  :alt: PyPI
  :target: https://pypi.org/project/teritorio
.. image:: https://pepy.tech/badge/teritorio
  :alt: Downloads
  :target: https://pepy.tech/project/teritorio
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style
  :target: https://github.com/psf/black

``teritorio`` two iterable singletons that ``Countries`` and ``Currencies``, that contain all the
relevant ISO information about countries and currencies, respectively.

In a nutshell
-------------

Installation
^^^^^^^^^^^^

The easiest way is to use `poetry`_ to manage your dependencies and add *teritorio* to them.
It requires Python 3.7.0+ to run.

.. code-block:: toml

    [tool.poetry.dependencies]
    teritorio = "*"

It is advised to always use the latest release, so that you'll get the latest ISO codes

Usage
^^^^^

There are two iterable singletons that can be imported from ``teritorio``: ``Countries`` and ``Currencies``.

.. code:: python

    from teritorio import Countries
    from teritorio import Currencies

Versioning
----------

The project project adheres to `Calendar Versioning`_.
The reason is that the data are dominated by political decisions,
making semantic versioning largely irrelevant.

Links
-----

- `Documentation`_
- `Changelog`_


.. _Calendar Versioning: https://calver.org
.. _poetry: https://python-poetry.org/
.. _Changelog: https://github.com/spapanik/teritorio/blob/main/CHANGELOG.rst
.. _Documentation: https://teritorio.readthedocs.io/en/latest/
