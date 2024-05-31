import sys
from importlib import import_module
from typing import Any


def cached_import(module_path: str, object_name: str) -> Any:
    """
    Imports or retrieves a specified module from the cache and returns the specified object.

    :param module_path: `str`
        Module path (dotted)

    :param object_name: `str`
        Object name

    :return: `Any`
        Specified object

    :raises:
        :raise ImportError: If the object is not defined in specified module
    """

    # Check whether module is loaded and fully initialized.
    module = sys.modules.get(module_path)
    spec = getattr(module, "__spec__", None)

    if not (module and spec and not getattr(spec, "_initializing", False)):
        module = import_module(module_path)

    try:
        return getattr(module, object_name)
    except AttributeError as error:
        raise ImportError(f"Attribute '{object_name}' is not defined in module '{module_path}'") from error


def import_object(object_path: str) -> Any:
    """
    Imports an object from module (with cache)

    :param object_path: `str`
        Object path in format '*.<module_name>.<object_name>'
    """

    try:
        module_path, object_name = object_path.rsplit('.', 1)
    except ValueError as error:
        raise ImportError("%s is not a module path" % object_path) from error

    return cached_import(
        module_path=module_path,
        object_name=object_name
    )
