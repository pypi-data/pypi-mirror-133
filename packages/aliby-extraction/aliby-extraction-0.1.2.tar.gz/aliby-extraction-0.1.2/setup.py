# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extraction',
 'extraction.core',
 'extraction.core.functions',
 'extraction.core.functions.custom',
 'extraction.examples']

package_data = \
{'': ['*'], 'extraction.examples': ['pairs_data/*']}

install_requires = \
['aliby-agora',
 'h5py==2.10',
 'more-itertools>=8.12.0,<9.0.0',
 'numpy>=1.17.3',
 'pandas>=1.3.5,<2.0.0',
 'py-find-1st>=1.1.5,<2.0.0',
 'scikit-image>=0.19.1',
 'scikit-learn==0.22.2.post1',
 'scipy>=1.4.1',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'aliby-extraction',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Alán Muñoz',
    'author_email': 'amuoz@ed.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
