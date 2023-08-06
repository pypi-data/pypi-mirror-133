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
    'version': '0.1.1',
    'description': 'Generate map descriptions for hiveworkshop.com',
    'long_description': 'Start with a config file:\n\n```yaml\n---\nmap_name: "Dota alstars"\nauthor: "feirfox"\nrepo_uri: null\ncontributing: null\nintroduction: |+\n  Dota is very fun game, league of legends stole from dota bascically\nscreenshots:\n  - caption: Invoker\n    uri: https://i.imgur.com/smX662W.jpeg\n  - caption: Pikachu\n    uri: https://i.imgur.com/Czgalle.jpeg\nicon_table:\n  title: "Heroes"\n  contents:\n    - caption: "Drow, likes to shot pewpew"\n      uri: https://i.imgur.com/XxEwZWP.png\nchangelog:\n  - version: 0.1.0\n    date: 16 Jul 1969\n    changes:\n      - Landed on the moon\ncredits:\n  - peq\n  - Frotty\n  - hiveworkshop\n```\n\nAnd generate a hive post:\n\n```shell\n./generate_submission_template.sh config.yaml\n```\n\nProduces:\n\n![Example post](screenshot.png)\n',
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
