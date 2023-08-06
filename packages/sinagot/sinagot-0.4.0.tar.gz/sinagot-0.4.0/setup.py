# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sinagot']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.6.3,<3.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'ray>=1.9.1,<2.0.0']

extras_require = \
{':extra == "draw"': ['numpy>=1.21.5,<2.0.0'],
 'draw': ['matplotlib>=3.5.1,<4.0.0', 'pydot>=1.4.2,<2.0.0']}

entry_points = \
{'console_scripts': ['test = tests.cli:run']}

setup_kwargs = {
    'name': 'sinagot',
    'version': '0.4.0',
    'description': 'Python lightweight workflow management framework with data exploration features',
    'long_description': '# Sinagot\n\n<p align="center">\n<a href="https://pypi.org/project/fastapi" target="_blank">\n    <img src="https://img.shields.io/pypi/v/sinagot?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/fastapi" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/sinagot.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n---\n\n**Source Code**: <a href="https://gitlab.com/YannBeauxis/sinagot" target="_blank">https://gitlab.com/YannBeauxis/sinagot</a>\n\n---\n\nSinagot is a Python lightweight workflow management framework using [Ray](https://www.ray.io/) as distributed computing engine.\n\nThe key features are:\n\n- **Easy to use**: Design workflow with simple Python classes and functions without external configuration files.\n- **Data exploration**: Access to computed data directly with object attributes, including complex type as pandas DataFrame.\n- **Scalable**: The [Ray](https://www.ray.io/) engine enable seamless scaling of workflows to external clusters.\n\n## Installation\n\n```bash\npip install sinagot\n```\n\n## Getting started\n\n```python\nimport pandas as pd\nfrom sinagot import Workspace, step, Item, seed, LocalStorage\n\n# Decorate functions to use them as step\n@step\ndef multiply(df: pd.DataFrame, factor: int) -> pd.DataFrame:\n    return df * factor\n\n\n@step\ndef get_single_data(df: pd.DataFrame) -> int:\n    return int(df.iloc[0, 0])\n\n\n# Design a workflow with a subclass of \'Item\'\nclass TestItem(Item):\n    raw_data: pd.DataFrame = seed()\n    factor: int = seed()\n    multiplied_data: pd.DataFrame = multiply.step(raw_data, factor=factor)\n    final_data: int = get_single_data.step(multiplied_data)\n\n\n# Create a \'Workspace\' subclass based on Item workflow with storage policy for data produced\nclass TestWorkspace(Workspace[TestItem]):\n    raw_data = LocalStorage("raw_data/data-{item_id}.csv")\n    factor = LocalStorage("params/factor")\n    multiplied_data = LocalStorage(\n        "computed/step-1-{item_id}.csv", write_kwargs={"index": False}\n    )\n    # In this example final_data is not stored and computed on demand\n\n\n# Create a workspace instance with local storage folder root path parameter\nws = TestWorkspace("/path/to/local_storage")\n\n# Access to a single item with its ID\nitem = ws["001"]\n\n# Access to item data, computed automatically if it does not exist in storage\ndisplay(item.multiplied_data)\nprint(item.final_data)\n```\n\nIn this example, the storage dataset is structured as follows :\n\n```\n├── params/\n│   └── factor\n├── raw_data/\n│   ├── data-{item_id}.csv\n│   └── ...\n└── computed/\n    ├── step-1-{item_id}.csv\n    └── ...\n```\n\nAnd the workflow is :\n\n<img src="docs/workflow.png" width="500">\n\n## Development Roadmap\n\nSinagot is at an early development stage but ready to be tested on actual datasets for workflows prototyping.\n\nFeatures development roadmap will be prioritized depending on usage feedbacks, so feel free to post an issue if you have any requirement.\n',
    'author': 'Yann Beauxis',
    'author_email': 'pro@yannbeauxis.net',
    'maintainer': 'Yann Beauxis',
    'maintainer_email': 'pro@yannbeauxis.net',
    'url': 'https://gitlab.com/YannBeauxis/sinagot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
