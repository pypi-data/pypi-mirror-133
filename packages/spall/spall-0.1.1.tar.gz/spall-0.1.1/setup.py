# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spall']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spall',
    'version': '0.1.1',
    'description': 'Object-oriented commandline',
    'long_description': 'spall\n======\n.. image:: https://github.com/jshwi/spall/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/spall/actions/workflows/ci.yml\n    :alt: ci\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/spall\n    :target: https://img.shields.io/pypi/v/spall\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/spall/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/spall\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nObject oriented commandline\n\n\nInstall\n-------\n\n``pip install spall``\n\nDevelopment\n\n``poetry install``\n\nExample Usage\n-------------\n\n.. code-block:: python\n\n    from spall import Subprocess\n\n    cmd = str(...)  # any command here e.g. git\n\n    proc = Subprocess(cmd)  # instantiate executable as object\n\n    passing = ...  # insert passing command here\n\n    returncode = proc.call(passing)  # this will print to console\n    print(returncode)  # -> 0\n\n    proc.call(passing, capture=True)  # this will record the output\n    proc.stdout()  # -> [...]\n\n    # stdout is consumed\n    proc.stdout()  # -> []\n\n    # this will record the output twice\n    proc.call(passing, capture=True)\n    proc.call(passing, capture=True)\n    proc.stdout()  # -> [..., ...]\n    proc.stdout()  # -> []\n\n     # this will redirect stdout to /dev/null\n    proc.call(passing, devnull=True)\n\n    # this will pipe stdout to file\n    proc.call(file="~/example.txt")\n\n    failing = ...  # insert failing command here\n\n    # will raise a ``subprocess.CalledProcessError``\n    returncode = proc.call(failing)\n    print(returncode)  # -> > 0\n\n    # this, however, will not\n    returncode = proc.call(failing, suppress=True)\n    print(returncode)  # -> > 0\n\n    # all the keyword arguments above can be set as the default for the\n    # instantiated object\n    proc = Subprocess(cmd, capture=True)\n\n    proc.call(passing)\n    proc.stdout()  # -> [...]\n\n    # but they will be overridden through the method\n    proc.call(passing, capture=False)\n    proc.stdout()  # -> []\n\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
