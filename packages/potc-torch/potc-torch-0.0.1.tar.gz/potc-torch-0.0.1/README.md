# potc-torch

[![PyPI](https://img.shields.io/pypi/v/potc-torch)](https://pypi.org/project/potc-torch/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/potc-torch)](https://pypi.org/project/potc-torch/)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/3e63a380eb43c56825d95931fd08ed61/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/3e63a380eb43c56825d95931fd08ed61/raw/comments.json)

[![Code Test](https://github.com/potc-dev/potc-torch/workflows/Code%20Test/badge.svg)](https://github.com/potc-dev/potc-torch/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/potc-dev/potc-torch/workflows/Badge%20Creation/badge.svg)](https://github.com/potc-dev/potc-torch/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/potc-dev/potc-torch/workflows/Package%20Release/badge.svg)](https://github.com/potc-dev/potc-torch/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/potc-dev/potc-torch/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/potc-dev/potc-torch)

[![GitHub stars](https://img.shields.io/github/stars/potc-dev/potc-torch)](https://github.com/potc-dev/potc-torch/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/potc-dev/potc-torch)](https://github.com/potc-dev/potc-torch/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/potc-dev/potc-torch)
[![GitHub issues](https://img.shields.io/github/issues/potc-dev/potc-torch)](https://github.com/potc-dev/potc-torch/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/potc-dev/potc-torch)](https://github.com/potc-dev/potc-torch/pulls)
[![Contributors](https://img.shields.io/github/contributors/potc-dev/potc-torch)](https://github.com/potc-dev/potc-torch/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/potc-dev/potc-torch)](https://github.com/potc-dev/potc-torch/blob/master/LICENSE)

[Potc](https://github.com/potc-dev/potc) support for torch module.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```
pip install potc-torch
```

## Quick Start

After `potc-torch` is installed, you can convert the `torch` objects into executable source code without any additional operations.

We can create a python script which is named `test_simple.py`

```python
import torch
from potc import transvars

a = torch.randn(2, 3)
b = torch.randint(-5, 10, (3, 4))
bs = b.size()
bd = b.device
if __name__ == '__main__':
    _code = transvars(
        {'a': a, 'b': b, 'bs': bs, 'bd': bd},
        reformat='pep8',
    )
    print(_code)

```

The output result should be like this (may be slightly different because of the usage of `torch.randn` and `torch.randint`)

```
import torch

__all__ = ['a', 'b', 'bd', 'bs']
a = torch.as_tensor(
    [[0.6224261522293091, 0.4725508689880371, 0.45328783988952637],
     [-0.5855962634086609, 0.4898407459259033, 0.4769541621208191]],
    dtype=torch.float32)
b = torch.as_tensor([[2, 7, 4, -3], [-2, 4, 8, 1], [7, -5, 3, 6]],
                    dtype=torch.long)
bd = torch.device('cpu')
bs = torch.Size([3, 4])
```

And, you can use the following CLI command to get the same output results as above.

```shell
potc export -v 'test_simple.a' -v 'test_simple.b*'
```



# Contributing

We appreciate all contributions to improve `potc` and `potc-torch`, both logic and system designs. Please refer to CONTRIBUTING.md for more guides.

# License

`potc-torch` released under the Apache 2.0 license.
