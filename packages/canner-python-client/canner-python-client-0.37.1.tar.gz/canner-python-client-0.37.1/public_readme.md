![pypi](https://img.shields.io/pypi/v/canner-python-client.svg)

# Introduction

This package provides a client interface to query Canner
a distributed SQL engine. It supports Python 3.6.x, 3.7.x and 3.8.x.

# Old package versions If needed

If you would like to download old versions which smaller than `0.37.x` ( < `0.37.x` ), please go to [cannerflow-python-client](https://pypi.org/project/cannerflow-python-client/) page.

# Installation

```
$ pip install canner-python-client
```

# Quick Start

## Client

```python
import canner
# bootstrap canner client with credentials
client = canner.client.bootstrap(
  endpoint='https://web.default.myname.apps.canner.com',
  workspace_id='444e8753-a4c0-4875-bdc0-834c79061d56',
  token='Y2xpZW50XzA0OTgzODM4LWNhZjktNGNmZi1hNDA4LWFkZDY3ZDc5MjIxNjo2N2YyNGY5OWEzYjFiZTEyZTg2MDI2MmMzNGQzZDRiYQ=='
)

# generate simple tpch query
query = client.gen_query('select * from tpch.tiny.region', data_format='list')
query.wait_for_finish()

# get all data with `get_all()` and data will be list of rows
data = query.get_all()
```

## Installing Issue

### Show `Couldn't find index page for 'xxx' (maybe misspelled?)` when installing dependency package `fastparquet` stage

If you're installing our `canner-python-client` by pip, and meet these message: `Couldn't find index page for 'xxx' (maybe misspelled?)`,e.g: `numpy`, `pytest-runner` followed the error `distutils.errors.DistutilsError: Could not find suitable distribution for Requirement.parse('xxxx')`,

then please install these package by hand through `pip install` command, and make sure the dependency package exist on PyPI, like below:

```bash
# If you face the issue for numpy
$> pip install numpy==1.19.5 # recommend version for our package

# If you face the issue for pytest-runner
$> pip install pytest-runner==5.3.0 # recommend version for our package
```

### Show `RuntimeError: Python version >= 3.7 required.` when installing dependency package `fastparquet` stage in Python 3.6.x

This error may happen on installing dependency package `fastparquet` stage and occurs when `fastparquet` install `numpy` version but it need `Python version >= 3.7` required,
You could install numpy `1.19.5` version (recommend) to prevent the issue.

## Learn more

Please learn more from

1. [Canner Official Document](https://flow.cannerdata.com/)
1. [Python Client Document](https://flow.cannerdata.com/docs/integration/development_python)
