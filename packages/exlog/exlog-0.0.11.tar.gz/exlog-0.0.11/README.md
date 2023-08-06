# exception-logging-decorator
The following function:
```py
from typing import NoReturn

from src.exlog.exceptlog import exception_logger

log = exception_logger("./tests/log.log", "US/Eastern")


@log
def no_return() -> NoReturn:
    """Test function."""
    raise Exception("DO NOT PASS GO DO NOT COLLECT $200.")


if __name__ == "__main__":
    try:
        no_return()
    except:
        pass
```
Logs the following exception in `log.log`.
```
ERROR:root:no_return
  raised Exception: DO NOT PASS GO DO NOT COLLECT $200.
    called with args = (), kwargs = {}
    at 2022-01-04 13:42:45.247324-05:00
Traceback (most recent call last):
  File "/home/ryan/pypi-packaging-tut/src/exlog/exceptlog.py", line 65, in wrapper
    output = function(*args, **kwargs)
  File "/home/ryan/pypi-packaging-tut/./tests/test.py", line 21, in no_return
    raise Exception("DO NOT PASS GO DO NOT COLLECT $200.")
Exception: DO NOT PASS GO DO NOT COLLECT $200.
```
