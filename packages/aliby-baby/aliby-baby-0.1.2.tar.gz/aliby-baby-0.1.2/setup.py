# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baby', 'baby.tracker', 'baby.training']

package_data = \
{'': ['*'], 'baby': ['models/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'imageio==2.8.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'scikit-image>=0.19.1,<0.20.0',
 'scikit-learn==0.22.2.post1',
 'tensorflow>=1.15,<=2.3',
 'tqdm>=4.62.3,<5.0.0',
 'tune-sklearn>=0.4.1,<0.5.0',
 'xgboost==1.4.2']

setup_kwargs = {
    'name': 'aliby-baby',
    'version': '0.1.2',
    'description': 'Birth Annotator for Budding Yeast',
    'long_description': None,
    'author': 'Julian Pietsch',
    'author_email': 'jpietsch@ed.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
