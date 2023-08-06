# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_cdk_update_checker']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['acuc = '
                     'aws_cdk_update_checker.main:fetch_aws_cdk_latest_version',
                     'aws_cdk_update_checker = '
                     'aws_cdk_update_checker.main:fetch_aws_cdk_latest_version']}

setup_kwargs = {
    'name': 'aws-cdk-update-checker',
    'version': '0.0.9',
    'description': 'This script fetches latest version of AWS CDK.',
    'long_description': None,
    'author': 'otajisan',
    'author_email': 'dev@morningcode.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/morning-code/aws-cdk-update-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
