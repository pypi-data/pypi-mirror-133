# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['purgatory',
 'purgatory.domain',
 'purgatory.domain.messages',
 'purgatory.service',
 'purgatory.service.handlers']

package_data = \
{'': ['*']}

extras_require = \
{'redis': ['aioredis>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'purgatory-circuitbreaker',
    'version': '0.5.0',
    'description': 'A circuit breaker implementation for asyncio',
    'long_description': 'Purgatory\n=========\n\n.. image:: https://github.com/mardiros/purgatory/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/mardiros/purgatory/actions/workflows/main.yml\n\n.. image:: https://codecov.io/gh/mardiros/purgatory/branch/main/graph/badge.svg?token=LFVOQC2C9E\n   :target: https://codecov.io/gh/mardiros/purgatory\n    \n\nA circuit breaker implementation for asyncio.\n',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/purgatory',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
