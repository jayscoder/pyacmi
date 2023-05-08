# pyacmi

TacView ACMI FileParser

**.acmi is a file used by tacview for creating flight recording from simulators or real world.

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
