# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['common_nb_preprocessors']

package_data = \
{'': ['*']}

install_requires = \
['nbconvert>=6.1,<7.0']

setup_kwargs = {
    'name': 'common-nb-preprocessors',
    'version': '0.0.10',
    'description': 'Inject metadata directly into jupyter notebook cells via _magic_ comments.',
    'long_description': '# Common Jupyter Notebook Preprocessors\n\nThis repository contains a personal collection of common notebook preprocessors.\nAs of writing, the most relevant function is probably:\n`common_nb_preprocessors.metadata_injector.jupyter_book_metadata_injector`\n\nThis function can be used to automatically inject [JupyterBook](https://jupyterbook.org/intro.html) specific tags into code-cells by using _magical_ comments.\nSet the function in the [nb_custom_formats](https://jupyterbook.org/file-types/jupytext.html) entry:\n\n```yaml\nsphinx:\n  config:\n    nb_custom_formats:\n        .ipynb:\n            - common_nb_preprocessors.metadata_injector.jupyter_book_metadata_injector\n```\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'snakemap_navigation@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/common_nb_preprocessors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
