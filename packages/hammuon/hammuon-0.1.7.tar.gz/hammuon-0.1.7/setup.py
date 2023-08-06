# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hammuon',
 'hammuon.hammuon',
 'hammuon.hammuon.data_structure',
 'hammuon.tests']

package_data = \
{'': ['*'], 'hammuon': ['dist/*']}

setup_kwargs = {
    'name': 'hammuon',
    'version': '0.1.7',
    'description': 'Basic and important data structures algorithms.',
    'long_description': '# Basic Data Structure Algorithms\n\n\n## 1. Quicksort\n## 2. Merge Sort\n## 3. Insertion Sort\n## 4. Bubble Sort\n## 5. Heapsort\n## 6. Counting Sort',
    'author': 'mcvarer',
    'author_email': 'ktuce.mcanv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcvarer/algorithms',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
