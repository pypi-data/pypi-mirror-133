# exception-logging-decorator

Creates an exception logging decorator that logs any exception that occurs in a function.

# Usage

The following function `no_return`:
```py
from typing import NoReturn

from exlog import exlog

log = exlog("./tests/log.log", "US/Eastern") # default timezone is UTC


@log
def no_return() -> NoReturn:
    """Test function."""
    raise Exception("zonks!")


if __name__ == "__main__":
    try:
        no_return()
    except:
        pass
```
Logs the following exception in `log.log`.
```
ERROR:root:no_return
  raised Exception: zonks!
    called with args = (), kwargs = {}
    at 2022-01-04 15:08:38.602817-05:00
Traceback (most recent call last):
  File "/home/ryan/exception-logging-decorator/src/exlog/exceptlog.py", line 65, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/exception-logging-decorator/./tests/test.py", line 23, in no_return
    raise Exception("zonks!")
Exception: zonks!
```

# Installation

```
pip install exlog
```
