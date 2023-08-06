# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['irpf_cei']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<9.0.0',
 'inquirer>=2.8.0,<3.0.0',
 'pandas>=1.3.0,<2.0.0',
 'xlrd>=1.2,<3.0']

entry_points = \
{'console_scripts': ['irpf-cei = irpf_cei.__main__:main']}

setup_kwargs = {
    'name': 'irpf-cei',
    'version': '3.5.2',
    'description': 'Programa auxiliar gratuito para calcular custos de ações, ETFs e fundos imobiliários.',
    'long_description': 'IRPF CEI\n========\n\n**NOTA: este programa foi completamente substituído pelo** `IRPF Investidor`_ **e não será mais atualizado.**\n\n.. _IRPF Investidor: https://github.com/staticdev/irpf-investidor/\n',
    'author': 'staticdev',
    'author_email': 'staticdev-support@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/irpf-cei',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
