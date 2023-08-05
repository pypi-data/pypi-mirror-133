# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['senvx', 'senvx.tests', 'senvx.tests.integration', 'senvx.tests.unit']

package_data = \
{'': ['*'], 'senvx.tests': ['static/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'ensureconda>=1.4.0,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['senvx = senvx.main:app']}

setup_kwargs = {
    'name': 'senvx',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Jorge',
    'author_email': 'jorge.girazabal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7.0,<3.10.0',
}


setup(**setup_kwargs)
