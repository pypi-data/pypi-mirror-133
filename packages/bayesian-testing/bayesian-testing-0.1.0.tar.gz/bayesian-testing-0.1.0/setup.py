# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayesian_testing',
 'bayesian_testing.experiments',
 'bayesian_testing.metrics',
 'bayesian_testing.utilities']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.0,<2.0.0']

setup_kwargs = {
    'name': 'bayesian-testing',
    'version': '0.1.0',
    'description': 'Bayesian A/B testing with simple probabilities.',
    'long_description': None,
    'author': 'Matus Baniar',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Matt52/bayesian-testing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
