# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secured_fields',
 'secured_fields.fields',
 'secured_fields.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=35', 'django>=3.1,<4.0']

setup_kwargs = {
    'name': 'django-secured-fields',
    'version': '0.1.1',
    'description': '',
    'long_description': '# django-secured-fields\n\n![GitHub](https://img.shields.io/github/license/C0D1UM/django-secured-fields)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/C0D1UM/django-secured-fields/CI)\n![PyPI](https://img.shields.io/pypi/v/django-secured-fields)  \n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-secured-fields)\n![Django Version](https://img.shields.io/badge/django-3.1%20%7C%203.2-blue)\n![PostgreSQL Version](https://img.shields.io/badge/postgres-12.9%20%7C%2013.5%20%7C%2014.1-blue)\n![MySQL Version](https://img.shields.io/badge/mysql-5.7%20%7C%208.0-blue)\n\nDjango encrypted fields with search enabled.\n\n# Usage\n\n_TBD_\n\n# Development\n\n## Requirements\n\n- Docker\n- Poetry\n- MySQL Client\n  - `brew install mysql-client`\n  - `echo \'export PATH="/usr/local/opt/mysql-client/bin:$PATH"\' >> ~/.bash_profile`\n\n## Running Project\n\n### Start backend databases\n\n```bash\nmake up-db\n```\n\n## Useful Commands\n\n### Linting\n\n```bash\nmake lint\n```\n\n### Testing\n\n```bash\nmake test\n```\n\n### Fix Formatting\n\n> Using `yapf`\n\n```bash\nmake yapf\n```\n',
    'author': 'CODIUM',
    'author_email': 'support@codium.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/C0D1UM/django-secured-fields',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
