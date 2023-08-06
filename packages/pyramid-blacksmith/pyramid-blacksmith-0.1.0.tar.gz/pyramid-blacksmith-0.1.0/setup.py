# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyramid_blacksmith']

package_data = \
{'': ['*']}

install_requires = \
['blacksmith>=0.9.2,<0.10.0', 'pyramid>=2.0,<3.0']

setup_kwargs = {
    'name': 'pyramid-blacksmith',
    'version': '0.1.0',
    'description': 'Pyramid Bindings for Blacksmith',
    'long_description': 'pyramid-blacksmith\n==================\n\n.. image:: https://readthedocs.org/projects/pyramid-blacksmith/badge/?version=latest\n   :target: https://pyramid-blacksmith.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/mardiros/pyramid-blacksmith/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/mardiros/pyramid-blacksmith/actions/workflows/main.yml\n   :alt: Continuous Integration\n\n.. image:: https://codecov.io/gh/mardiros/pyramid-blacksmith/branch/main/graph/badge.svg?token=9IRABRO2LN\n   :target: https://codecov.io/gh/mardiros/pyramid-blacksmith\n   :alt: Coverage\n\nPyramid bindings for `Blacksmith`_ rest api client.\n\n\nIntroduction\n------------\n\nThis plugin create a request proterty named ``blacksmith`` that bind\nclients to do API Call using `Blacksmith`_ \n\n\nClients are configured via the pyramid configurator and its settings.\n\n\n.. _`Blacksmith`: https://pypi.org/project/blacksmith/\n\n',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/pyramid-blacksmith',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
