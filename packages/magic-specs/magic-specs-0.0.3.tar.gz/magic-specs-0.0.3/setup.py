# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_specs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'magic-specs',
    'version': '0.0.3',
    'description': '',
    'long_description': '# Magic value specification utilities\n\n[![Coverage Status](https://coveralls.io/repos/github/MrThearMan/magic-specs/badge.svg?branch=main)](https://coveralls.io/github/MrThearMan/magic-specs?branch=main)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/MrThearMan/magic-specs/Tests)](https://github.com/MrThearMan/magic-specs/actions/workflows/main.yml)\n[![PyPI](https://img.shields.io/pypi/v/magic-specs)](https://pypi.org/project/magic-specs)\n[![GitHub](https://img.shields.io/github/license/MrThearMan/magic-specs)](https://github.com/MrThearMan/magic-specs/blob/main/LICENSE)\n[![GitHub last commit](https://img.shields.io/github/last-commit/MrThearMan/magic-specs)](https://github.com/MrThearMan/magic-specs/commits/main)\n[![GitHub issues](https://img.shields.io/github/issues-raw/MrThearMan/magic-specs)](https://github.com/MrThearMan/magic-specs/issues)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/magic-specs)](https://pypi.org/project/magic-specs)\n\n```shell\npip install magic_specs\n```\n---\n\n**Documentation**: [https://mrthearman.github.io/magic-specs/](https://mrthearman.github.io/magic-specs/)\n\n**Source Code**: [https://github.com/MrThearMan/magic-specs](https://github.com/MrThearMan/magic-specs)\n\n---\n\nThis library contains utilities for making definitions for magic values.\n\n',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrThearMan/magic-specs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
