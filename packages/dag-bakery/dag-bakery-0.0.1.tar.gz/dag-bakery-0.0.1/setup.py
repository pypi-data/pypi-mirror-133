# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dag_bakery']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow==1.10.15']

setup_kwargs = {
    'name': 'dag-bakery',
    'version': '0.0.1',
    'description': 'Dag Bakery enables the capability to define Airflow DAGs via YAML',
    'long_description': None,
    'author': 'Data Platform',
    'author_email': 'data.platform@typeform.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
