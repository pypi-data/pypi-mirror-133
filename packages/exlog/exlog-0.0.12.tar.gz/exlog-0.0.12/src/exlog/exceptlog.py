"""Second order exception logging decorator.

Creates exception loggers that log any exception that occurs in a function
at the provided log file location. Logged information includes: qualified
function name, the error name, the error, args, kwargs, and the timestamp
in UTC (or in the timezone provided). Errors are re-raised after logging.

  Typical usage example:

  log = exception_logger("./log.log", "US/Eastern")
  @log
  def no_return() -> NoReturn: raise Exception
"""

import datetime
import functools
import logging
import pathlib
import sys
from typing import Any, Callable, TypeVar

if (sys.version_info.major, sys.version_info.minor) < (3, 6):
    raise Exception("Python 3.6+ required for zoneinfo.")
elif sys.version_info.minor < 9:
    import backports.zoneinfo

    _zoneinfo = backports.zoneinfo
else:
    import zoneinfo

    _zoneinfo = zoneinfo

from mypy_extensions import KwArg, VarArg

F = TypeVar("F", bound=Callable[[VarArg(Any), KwArg(Any)], Any])


def exception_logger(filepath: str, timezone: str = "Etc/UTC") -> Callable[[F], F]:
    """Creates exception logging decorators.

    Args:
        filepath: Path for created decorator to log exception. Deletes old log file
        if needed.
        timezone: A tz database timezone name.

    Returns:
        Decorator that logs info of an exception which occurs in a function then
        re-raise the exception.
    """
    _filepath = pathlib.Path(filepath).absolute()
    try:
        _filepath.unlink()
    except FileNotFoundError:
        pass
    logging.basicConfig(filename=str(_filepath), filemode="a", force=True, level=logging.ERROR)
    logger = logging.getLogger()

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            timestamp = str(
                datetime.datetime.now().astimezone(_zoneinfo.ZoneInfo(timezone))
            )
            try:
                output = function(*args, **kwargs)
                return output
            except Exception as error:
                logger.exception(
                    f"{function.__qualname__}\n"
                    f"  raised {error.__class__.__name__}: {str(error)}\n"
                    f"    called with args = {args}, kwargs = {kwargs}\n"
                    f"    at {timestamp}\n"
                )
                raise

        return wrapper

    return decorator
