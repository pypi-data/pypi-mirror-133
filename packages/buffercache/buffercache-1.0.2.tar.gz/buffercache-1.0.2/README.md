![GitHub](https://img.shields.io/github/license/caibingcheng/buffercache)
![GitHub branch checks state](https://img.shields.io/github/checks-status/caibingcheng/buffercache/master)
![GitHub Release Date](https://img.shields.io/github/release-date/caibingcheng/buffercache)

buffercache is a python3 library. It provides utility methods for data caching.

buffercache supports Python 3.0+ only. It is contained in only one Python file, so it can be easily copied into your project. (The copyright and license notice must be retained.)

example:

```python
from buffercache import BufferCache as BC

set_data = ((1, 2, 3), None, "", "123", (), [], {})

def get(data, args):
    return data, args

bc = BC(timeout=0).set_getter(get)
for data in set_data:
    bc.update(data, {'key': data})
    print(bc.get())
```

Bugs can be reported to [https://github.com/caibingcheng/buffercache](https://github.com/caibingcheng/buffercache). The code can also be found there.