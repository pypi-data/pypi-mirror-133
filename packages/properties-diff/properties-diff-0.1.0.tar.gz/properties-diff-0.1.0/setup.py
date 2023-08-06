# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['properties_diff']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

entry_points = \
{'console_scripts': ['properties-diff = properties_diff.cli:run']}

setup_kwargs = {
    'name': 'properties-diff',
    'version': '0.1.0',
    'description': 'Command line tool to compare properties files',
    'long_description': '![Github](https://img.shields.io/github/tag/essembeh/properties-diff.svg)\n![PyPi](https://img.shields.io/pypi/v/properties-diff.svg)\n![Python](https://img.shields.io/pypi/pyversions/properties-diff.svg)\n\n\n# properties-diff\n\nCommand line tool to compare *properties* files and print differences with colors as if you were using `diff` or `colordiff` tools.\n\n![Example](capture.png)\n\n\n# Install\n\nInstall from the sources\n```sh\n$ pip3 install --user --upgrade git+https://github.com/essembeh/properties-diff\n$ properties-diff path/to/file.properties path/to/another/file.properties\n```\n\nInstall the latest release from [PyPI](https://pypi.org/properties-diff)\n```sh\n$ pip3 install --user --upgrade properties-diff\n$ properties-diff path/to/file.properties path/to/another/file.properties\n```\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/essembeh/properties-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
