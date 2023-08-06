# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hammuon', 'hammuon.data_structure', 'hammuon.metrics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hammuon',
    'version': '0.1.11',
    'description': 'Basic and important data structures algorithms.',
    'long_description': '# Basic Data Strcutre Algorithms\n\n## Installing\n\n```bash\npip install hammuon\n``` \nor \n```bash\npip install -e git+https://github.com/mcvarer/algorithms.git#egg=hammuon\n```\n\n\n## 1. Quick Sort\nQuick Sort is a sorting algorithm, which is commonly used in computer science. \nQuick Sort is a divide and conquer algorithm. \n\n### Usage\n```python\nfrom hammuon.data_structure.quick_sort import quickSort\n\nprint(quickSort([8, 12, 55, -12]))\n```\n\n### Output\n```bash\n[-12, 8, 12, 55]\n```\n\n## 2. Bubble Sort\nBubble sort is a sorting algorithm that compares two adjacent\nelements and swaps them until they are not in the intended order.\n\n### Usage\n```python\nfrom hammuon.data_structure.bubble_sort import bubbleSort\n\nprint(bubbleSort([8, 12, 55, -12]))\n```\n\n### Output\n```bash\n[-12, 8, 12, 55]\n```\n\n## 3. Selection Sort\nSelection sort is a simple sorting algorithm.\n\n### Usage\n```python\nfrom hammuon.data_structure.selection_sort import selectionSort\n\nprint(selectionSort([8, 12, 55, -12]))\n```\n\n### Output\n```bash\n[-12, 8, 12, 55]\n```',
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
