# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compsyn']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'black>=21.12b0,<22.0',
 'boto3>=1.20.30,<2.0.0',
 'google-api-core>=2.3.2,<3.0.0',
 'google-auth>=2.3.3,<3.0.0',
 'google-cloud-vision>=2.6.3,<3.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'googleapis-common-protos>=1.54.0,<2.0.0',
 'grpcio>=1.43.0,<2.0.0',
 'ipykernel>=6.6.1,<7.0.0',
 'ipython>=7.31.0,<8.0.0',
 'kymatio>=0.2.1,<0.3.0',
 'matplotlib>=3.5.1,<4.0.0',
 'memory-profiler>=0.60.0,<0.61.0',
 'nltk>=3.6.7,<4.0.0',
 'notebook>=6.4.6,<7.0.0',
 'numba>=0.54.1,<0.55.0',
 'pandas>=1.3.5,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-depends>=1.0.1,<2.0.0',
 'pytest>=6.2.5,<7.0.0',
 'qloader>=8.1.4,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'scikit-image>=0.19.1,<0.20.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'textblob>=0.17.1,<0.18.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'compsyn',
    'version': '1.0.1',
    'description': 'python package to explore the color of language',
    'long_description': None,
    'author': 'comp-syn',
    'author_email': 'group@comp-syn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
