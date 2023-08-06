# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thw_submission_generator']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.17.20,<0.18.0']

entry_points = \
{'console_scripts': ['thw-submission-generator = '
                     'thw_submission_generator:main']}

setup_kwargs = {
    'name': 'thw-submission-generator',
    'version': '0.1.0',
    'description': 'Generate map descriptions for hiveworkshop.com',
    'long_description': None,
    'author': 'Cokemonkey11',
    'author_email': 'Cokemonkey11@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
