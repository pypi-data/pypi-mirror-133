# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_sqs_consumer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.0,<2.0.0',
 'botocore>=1.20.0,<2.0.0',
 'single-source>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'aws-sqs-consumer',
    'version': '0.0.12',
    'description': 'AWS SQS Consumer',
    'long_description': None,
    'author': 'Flyweight Group',
    'author_email': 'nobody@flyweightgroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
