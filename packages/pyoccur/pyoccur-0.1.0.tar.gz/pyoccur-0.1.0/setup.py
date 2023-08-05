# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyoccur']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyoccur',
    'version': '0.1.0',
    'description': 'Operations with duplicates in python lists',
    'long_description': "# pyoccur\n\n## Python Occurrence Operations on Lists\n\n### About Package\nA simple python package with 3 functions\n\n* has_dup(<listparam>)\n* get_dup(<listparam>)\n* remove_dup(<listparam>)\n\nCurrently the duplicate operation functions can operate on list of elements with below data types\n\n* str\n* int\n* float\n* dict\n* list\n* pandas.DataFrame\n\n### Example\n```\nfrom pyoccur import pyoccur\nl1 = ['abc',123,'def','abc',22,10]\nl2 = [{'abc':100},'wee',123,{'abc':100},'abc',123,{'a':1,'b':2}]\npyoccur.has_dup(l1)\n# Output: True\npyoccur.get_dup(l2)\n# Output: [{'abc':100},123]\n```\n\n### Contributing\n- Feel free to raise PR to add your contributions\n- Do raise issues if found any, in the Github Issues\n",
    'author': 'amrs-tech',
    'author_email': 'amrs.tech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amrs-tech/pyoccur/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
