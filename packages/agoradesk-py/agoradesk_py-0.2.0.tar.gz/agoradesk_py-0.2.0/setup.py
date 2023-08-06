# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agoradesk_py']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.1,<2.0.0', 'httpx>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'agoradesk-py',
    'version': '0.2.0',
    'description': 'Python Interface for Agoradesk.com and LocalMonero.co API',
    'long_description': None,
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
