import logging
from contextlib import contextmanager
from traceback import format_exception
from typing import Union, Type, Tuple, Generator

_logger = logging.getLogger(__name__)


def get_traceback_text(error: BaseException) -> str:
    """
    Returns traceback text

    :param error: `BaseException`
        Exception

    :return: `str`
        Traceback text
    """

    return "".join(format_exception(type(error), error, error.__traceback__))


@contextmanager
def supress_exception(exception: Union[Type[BaseException], Tuple[Type[BaseException], ...]], log: bool = False) -> Generator[None, None, None]:
    try:
        yield
    except exception as error:
        if log:
            _logger.debug(f"Suppressing exception {error.__class__.__name__}: {error}")
