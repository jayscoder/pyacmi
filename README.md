# pyacmi: TacView ACMI FileParser

[![PyPI Latest Release](https://img.shields.io/pypi/v/pyacmi.svg)](https://pypi.org/project/pyacmi/)
[![License](https://img.shields.io/pypi/l/pyacmi.svg)](https://github.com/wangtong2015/pyacmi)
[![Package Status](https://img.shields.io/pypi/status/pyacmi.svg)](https://pypi.org/project/pyacmi/)

`**.acmi` is a file used by tacview for creating flight recording from simulators or real world.

The source code is currently hosted on GitHub at: https://github.com/wangtong2015/pyacmi

## Install

```shell

pip install pyacmi

```

## Example

```python

from pyacmi import *

acmi = Acmi('test.acmi')
print(acmi)

```

## Credits

- [https://github.com/rp-/acmi](https://github.com/rp-/acmi)
