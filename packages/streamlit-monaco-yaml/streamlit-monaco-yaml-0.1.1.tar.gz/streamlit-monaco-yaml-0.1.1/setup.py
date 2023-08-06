# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_monaco_yaml']

package_data = \
{'': ['*'], 'streamlit_monaco_yaml': ['frontend-build/*']}

install_requires = \
['streamlit>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-monaco-yaml',
    'version': '0.1.1',
    'description': 'Monaco editor component for Streamlit for editing YAML files.',
    'long_description': None,
    'author': 'Skalar Systems',
    'author_email': 'contact@skalarsystems.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
