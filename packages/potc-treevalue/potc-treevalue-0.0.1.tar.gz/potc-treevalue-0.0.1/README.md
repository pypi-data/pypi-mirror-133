# potc-treevalue

[![PyPI](https://img.shields.io/pypi/v/potc-treevalue)](https://pypi.org/project/potc-treevalue/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/potc-treevalue)](https://pypi.org/project/potc-treevalue/)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/3a975cb01e1a4ec1bc363ec8049485b9/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/3a975cb01e1a4ec1bc363ec8049485b9/raw/comments.json)

[![Code Test](https://github.com/potc-dev/potc-treevalue/workflows/Code%20Test/badge.svg)](https://github.com/potc-dev/potc-treevalue/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/potc-dev/potc-treevalue/workflows/Badge%20Creation/badge.svg)](https://github.com/potc-dev/potc-treevalue/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/potc-dev/potc-treevalue/workflows/Package%20Release/badge.svg)](https://github.com/potc-dev/potc-treevalue/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/potc-dev/potc-treevalue/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/potc-dev/potc-treevalue)

[![GitHub stars](https://img.shields.io/github/stars/potc-dev/potc-treevalue)](https://github.com/potc-dev/potc-treevalue/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/potc-dev/potc-treevalue)](https://github.com/potc-dev/potc-treevalue/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/potc-dev/potc-treevalue)
[![GitHub issues](https://img.shields.io/github/issues/potc-dev/potc-treevalue)](https://github.com/potc-dev/potc-treevalue/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/potc-dev/potc-treevalue)](https://github.com/potc-dev/potc-treevalue/pulls)
[![Contributors](https://img.shields.io/github/contributors/potc-dev/potc-treevalue)](https://github.com/potc-dev/potc-treevalue/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/potc-dev/potc-treevalue)](https://github.com/potc-dev/potc-treevalue/blob/master/LICENSE)

[Potc](https://github.com/potc-dev/potc) support for treevalue module.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```
pip install potc-treevalue
```

## Quick Start

After `potc-treevalue` is installed, you can convert the `treevalue` objects into executable source code without any additional operations.

We can create a python script which is named `test_simple.py`

```python
from potc import transvars
from treevalue import FastTreeValue, raw

r = raw({'a': 1, 'b': 2, 'c': [3, 4]})
t = FastTreeValue({
    'a': 1, 'b': 'this is a string',
    'c': [], 'd': {
        'x': raw({'a': 1, 'b': (None, Ellipsis)}),
        'y': {3, 4, 5}
    }
})
st = t._detach()
if __name__ == '__main__':
    _code = transvars(
        {'t': t, 'st': t._detach(), 'r': r},
        reformat='pep8'
    )
    print(_code)

```

The output result should be like this

```
from treevalue import FastTreeValue, raw
from treevalue.tree.common import create_storage

__all__ = ['r', 'st', 't']
r = raw({'a': 1, 'b': 2, 'c': [3, 4]})
st = create_storage({
    'a': 1,
    'b': 'this is a string',
    'c': [],
    'd': {
        'x': raw({
            'a': 1,
            'b': (None, ...)
        }),
        'y': {3, 4, 5}
    }
})
t = FastTreeValue({
    'a': 1,
    'b': 'this is a string',
    'c': [],
    'd': {
        'x': raw({
            'a': 1,
            'b': (None, ...)
        }),
        'y': {3, 4, 5}
    }
})
```

And, you can use the following CLI command to get the same output results as above.

```shell
potc export -v 'test_simple.t' -v 'test_simple.st' -v 'test_simple.r'
```


# Contributing

We appreciate all contributions to improve `potc` and `potc-treevalue`, both logic and system designs. Please refer to CONTRIBUTING.md for more guides.

# License

`potc-treevalue` released under the Apache 2.0 license.
