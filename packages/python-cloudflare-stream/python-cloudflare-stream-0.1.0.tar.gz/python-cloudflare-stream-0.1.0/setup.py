# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_cloudflare_stream']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'python-cloudflare-stream',
    'version': '0.1.0',
    'description': "A Python wrapper for Cloudflare Stream's API",
    'long_description': '########################\npython-cloudflare-stream\n########################\n\nPackage setup, installation and examples available at https://github.com/arbington/python-cloudflare-stream\n',
    'author': 'Kalob Taulien',
    'author_email': 'kalob.taulien@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arbington/python-cloudflare-stream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
