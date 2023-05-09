# pyacmi: TacView ACMI FileParser

[![PyPI Latest Release](https://img.shields.io/pypi/v/pyacmi.svg)](https://pypi.org/project/pyacmi/)
[![License](https://img.shields.io/pypi/l/pyacmi.svg)](https://github.com/wangtong2015/pyacmi)
[![Package Status](https://img.shields.io/pypi/status/pyacmi.svg)](https://pypi.org/project/pyacmi/)

`**.acmi` is a file used by tacview for creating flight recording from simulators or real world.

The source code is currently hosted on GitHub at: https://github.com/wangtong2015/pyacmi

ACMI file Introduction:  [Tacview - ACMI flight recordings.md](Tacview - ACMI flight recordings.md)

## Installation

You can install pyacmi via pip or pip3 for Python 3+:

```shell
$ pip3 install pyacmi
```

You can install a specific version of pyacmi by:

```shell
$ pip3 install pyacmi==1.1.0
```

You can upgrade pyacmi to the latest version by:

```shell
$ pip3 install --upgrade pyacmi
```

## Example

```python

from pyacmi import Acmi

acmi = Acmi('test.acmi')
print(acmi)

print(acmi.reference_latitude, acmi.reference_longitude, acmi.reference_time)

# 打印所有的object
for obj_id in acmi.objects:
    obj = acmi.objects[obj_id]
    print(obj)
    print(obj.id, obj.name, obj.country, obj.tags, obj.type)

# 导出成csv
acmi.export_csv('test.csv', remove_empty=True, export_obj_ids=None)
```

## Credits

- [https://github.com/rp-/acmi](https://github.com/rp-/acmi)
