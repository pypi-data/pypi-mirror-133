# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deep_sorted']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deep-sorted',
    'version': '0.0.1',
    'description': 'Sorting of nested dicts and lists',
    'long_description': '# deep-sorted\n\n![Testing and linting](https://github.com/danhje/deep-sorted/workflows/Test%20And%20Lint/badge.svg)\n[![codecov](https://codecov.io/gh/danhje/deep-sorted/branch/master/graph/badge.svg)](https://codecov.io/gh/danhje/deep-sorted)\n![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/danhje/deep-sorted?include_prereleases)\n![PyPI](https://img.shields.io/pypi/v/deep-sorted)\n\n## Motivation\n\n...\n\n## Installation\n\nUsing poetry:\n\n```shell\npoetry add deep-sorted\n```\n\nUsing pipenv:\n\n```shell\npipenv install deep-sorted\n```\n\nUsing pip:\n\n```shell\npip install deep-sorted\n```\n\n## Usage\n\n```python\nfrom deep_sorted import deep_sorted\n```\n',
    'author': 'Daniel Hjertholm',
    'author_email': 'daniel.hjertholm@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danhje/deep-sorted',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
