# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hammuon', 'hammuon.data_structure']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hammuon',
    'version': '0.1.0',
    'description': 'Basic and important data structures algorithm',
    'long_description': '# Basic Algorithms\n\n\n## 1. Quick Sort\nQuick Sort is a sorting algorithm, which is commonly used in computer science. \nQuick Sort is a divide and conquer algorithm. \n\n### Usage\n```python\nfrom data_structure import quickSort\n\nprint(quickSort([8, 12, 55, -12]))\n```\n\n### Output\n```bash\n[-12, 8, 12, 55]\n```',
    'author': 'mcvarer',
    'author_email': 'ktuce.mcanv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
