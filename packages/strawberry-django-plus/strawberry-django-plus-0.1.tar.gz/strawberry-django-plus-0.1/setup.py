# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django_plus',
 'strawberry_django_plus.gql',
 'strawberry_django_plus.utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0',
 'strawberry-graphql-django>=0.2.5,<0.3.0',
 'strawberry-graphql>=0.93.4,<0.94.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'strawberry-django-plus',
    'version': '0.1',
    'description': 'Enhanced Strawberry GraphQL integration with Django',
    'long_description': '# strawberry-django-plus\n\n[![build status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fblb-ventures%2Fstrawberry-django-plus%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/blb-ventures/straw/goto?ref=master)\n[![docs status](https://img.shields.io/readthedocs/strawberry-django-plus.svg)](https://strawberry-django-plus.readthedocs.io)\n[![coverage](https://img.shields.io/codecov/c/github/blb-ventures/strawberry-django-plus.svg)](https://codecov.io/gh/blb-ventures/strawberry-django-plus)\n[![PyPI version](https://img.shields.io/pypi/v/strawberry-django-plus.svg)](https://pypi.org/project/strawberry-django-plus/)\n![python version](https://img.shields.io/pypi/pyversions/strawberry-django-plus.svg)\n![django version](https://img.shields.io/pypi/djversions/strawberry-django-plus.svg)\n',
    'author': 'Thiago Bellini Ribeiro',
    'author_email': 'thiago@bellini.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blb-ventures/strawberry-django-plus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
