# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaud']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.3.2,<5.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'black>=21.12b0,<22.0',
 'codecov>=2.1.12,<3.0.0',
 'coverage>=6.2,<7.0',
 'docformatter>=1.4,<2.0',
 'environs>=9.4.0,<10.0.0',
 'flynt>=0.75,<0.76',
 'isort>=5.10.1,<6.0.0',
 'm2r>=0.2.1,<0.3.0',
 'mistune<=0.8.4',
 'mypy>=0.930,<0.931',
 'object-colors>=2.0.1,<3.0.0',
 'pipfile-requirements>=0.3.0,<0.4.0',
 'pylint>=2.12.2,<3.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=6.2.5,<7.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'readmetester>=1.0.1,<2.0.0',
 'sphinxcontrib-fulltoc>=1.2.0,<2.0.0',
 'sphinxcontrib-programoutput>=0.17,<0.18',
 'toml>=0.10.2,<0.11.0',
 'vulture>=2.3,<3.0']

entry_points = \
{'console_scripts': ['pyaud = pyaud.__main__:main']}

setup_kwargs = {
    'name': 'pyaud',
    'version': '3.7.0',
    'description': 'Framework for writing Python package audits',
    'long_description': None,
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
