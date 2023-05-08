# pyacmi: TacView ACMI FileParser

[![PyPI Latest Release](https://img.shields.io/pypi/v/pyacmi.svg)](https://pypi.org/project/pyacmi/)

`**.acmi` is a file used by tacview for creating flight recording from simulators or real world.

借鉴了[https://github.com/rp-/acmi](https://github.com/rp-/acmi)

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
