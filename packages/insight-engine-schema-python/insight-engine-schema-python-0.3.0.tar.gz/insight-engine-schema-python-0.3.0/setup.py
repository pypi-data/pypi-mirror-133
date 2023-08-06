# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema', 'schema.legacy']

package_data = \
{'': ['*']}

install_requires = \
['fhir.resources>=6.0,<7.0']

setup_kwargs = {
    'name': 'insight-engine-schema-python',
    'version': '0.3.0',
    'description': 'Rialtic insight engine schema in Python',
    'long_description': '# Rialtic insight engine schema in Python\n\nThis repo contains translation of InsightEngine Request/Response schema to Python.\nIt uses `fhir.resources` internally (see https://pypi.org/project/fhir.resources/).\n\ninstall with `pip install insight-engine-schema`\n\n',
    'author': 'Rialtic',
    'author_email': 'engines.data@rialtic.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rialtic.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
