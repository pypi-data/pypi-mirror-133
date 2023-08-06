# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['correios_utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'correios-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Correios Python 🚚\n\n> **correios-py** - Biblioteca para a realização de cotação de frete de encomendas no serviço dos Correios\n',
    'author': 'Douglas Gusson',
    'author_email': 'douglasgusson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
