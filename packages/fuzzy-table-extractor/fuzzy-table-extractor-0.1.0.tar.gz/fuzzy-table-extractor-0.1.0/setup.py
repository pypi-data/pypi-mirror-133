# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_table_extractor', 'fuzzy_table_extractor.tests']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.2,<2.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'pandas>=1.3.5,<2.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'python-docx>=0.8.11,<0.9.0',
 'pywin32>=303,<304']

setup_kwargs = {
    'name': 'fuzzy-table-extractor',
    'version': '0.1.0',
    'description': 'A tool to extract tables from documents using fuzzy matching',
    'long_description': '# DocxTableExtractor\nA tool to extract tables from .docx files\n',
    'author': 'Leonardo Sirino',
    'author_email': 'leonardosirino@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
