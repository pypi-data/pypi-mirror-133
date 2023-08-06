# Sinagot

<p align="center">
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/sinagot?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sinagot.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Source Code**: <a href="https://gitlab.com/YannBeauxis/sinagot" target="_blank">https://gitlab.com/YannBeauxis/sinagot</a>

---

Sinagot is a Python lightweight workflow management framework using [Ray](https://www.ray.io/) as distributed computing engine.

The key features are:

- **Easy to use**: Design workflow with simple Python classes and functions without external configuration files.
- **Data exploration**: Access to computed data directly with object attributes, including complex type as pandas DataFrame.
- **Scalable**: The [Ray](https://www.ray.io/) engine enable seamless scaling of workflows to external clusters.

## Installation

```bash
pip install sinagot
```

## Getting started

```python
import pandas as pd
from sinagot import Workspace, step, Item, seed, LocalStorage

# Decorate functions to use them as step
@step
def multiply(df: pd.DataFrame, factor: int) -> pd.DataFrame:
    return df * factor


@step
def get_single_data(df: pd.DataFrame) -> int:
    return int(df.iloc[0, 0])


# Design a workflow with a subclass of 'Item'
class TestItem(Item):
    raw_data: pd.DataFrame = seed()
    factor: int = seed()
    multiplied_data: pd.DataFrame = multiply.step(raw_data, factor=factor)
    final_data: int = get_single_data.step(multiplied_data)


# Create a 'Workspace' subclass based on Item workflow with storage policy for data produced
class TestWorkspace(Workspace[TestItem]):
    raw_data = LocalStorage("raw_data/data-{item_id}.csv")
    factor = LocalStorage("params/factor")
    multiplied_data = LocalStorage(
        "computed/step-1-{item_id}.csv", write_kwargs={"index": False}
    )
    # In this example final_data is not stored and computed on demand


# Create a workspace instance with local storage folder root path parameter
ws = TestWorkspace("/path/to/local_storage")

# Access to a single item with its ID
item = ws["001"]

# Access to item data, computed automatically if it does not exist in storage
display(item.multiplied_data)
print(item.final_data)
```

In this example, the storage dataset is structured as follows :

```
├── params/
│   └── factor
├── raw_data/
│   ├── data-{item_id}.csv
│   └── ...
└── computed/
    ├── step-1-{item_id}.csv
    └── ...
```

And the workflow is :

<img src="docs/workflow.png" width="500">

## Development Roadmap

Sinagot is at an early development stage but ready to be tested on actual datasets for workflows prototyping.

Features development roadmap will be prioritized depending on usage feedbacks, so feel free to post an issue if you have any requirement.
