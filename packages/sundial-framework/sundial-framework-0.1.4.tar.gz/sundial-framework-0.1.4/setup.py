# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sundial']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'numpy',
 'pandas>=1.2.5,<2.0.0',
 'plotly>=5.2.2,<6.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'tensorflow>=2.6.0,<3.0.0']

setup_kwargs = {
    'name': 'sundial-framework',
    'version': '0.1.4',
    'description': 'The Sundial timeseries model data framework.',
    'long_description': None,
    'author': 'Gavin Bell',
    'author_email': 'gavin.bell@optimeering.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
