import os
from typing import Any, Dict

from src.core.utils.lazy_objects import AbstractLazyObject, LazyObject, LazyInstance
from src.core.utils.types import MISSING
from .config import AbstractConfig, PyModuleConfig
from .exceptions import ConfigurationError


class ProjectSettings:
    """
    Manages project settings using various configurations (used in `setup_from_environment` method)

    Class Attributes:
    - `ENVIRONMENT_VARIABLE: str`
        The environment variable used to specify the configuration module.

    - `LAZY_OBJECT_PREFIX: str`
        Prefix used to identify lazy objects in settings.

    - `LAZY_INSTANCE_PREFIX: str`
        Prefix used to identify lazy instances in settings.

    Methods:
    - `__init__(self) -> None`
        Initializes the ProjectSettings instance.

    - `__getattr__(self, item: str) -> Any`
        Overrides the attribute getter to dynamically fetch values from registered configurations.

    - `__setattr__(self, key: str, value: Any) -> None`
        Overrides the default `__setattr__` method to handle attribute assignments.
        Set the specified attribute `key` to the provided value in the `_config_data`.

    - `_get_value_from_config_data(self, item: str) -> Any`
        Retrieves a value from `_config_data`, handling lazy objects and lazy instances.

    - `register_config(self, config: AbstractConfig) -> None`
        Loads and registers config values to the project config

    - `setup_from_environment(self) -> None`
        Sets up PyModuleConfig based on the specified environment variable.
    """

    ENVIRONMENT_VARIABLE: str = "CONFIG_MODULE"

    LAZY_OBJECT_PREFIX: str = "lazyobj."
    LAZY_INSTANCE_PREFIX: str = "lazyins."

    def __init__(self) -> None:
        """
        Initializes the ProjectSettings instance.
        """

        self._config_data: Dict[str, Any] = {}

    def _get_value_from_config_data(self, item: str) -> Any:
        """
        Retrieves a value from `_config_data`

        :param item: `str`
            The attribute name.

        :return: `Any`
            The retrieved value

        :raises:
            :raise KeyError: If `_config_data` has no key `item`
        """

        value = self._config_data[item]

        if isinstance(value, AbstractLazyObject):
            return value.get()
        elif isinstance(value, str) and value.startswith(self.__class__.LAZY_OBJECT_PREFIX):
            lazy_object = LazyObject[Any](".".join(value.split(".")[1:]))
            setattr(self, item, lazy_object)
            return lazy_object.get()
        elif isinstance(value, tuple) and (len(value) != 0 and isinstance(value[0], str) and value[0].startswith(self.__class__.LAZY_INSTANCE_PREFIX)):
            name, *args = value
            lazy_instance = LazyInstance[Any](".".join(name.split(".")[1:]), *args)
            setattr(self, item, lazy_instance)
            return lazy_instance.get()

        return value

    def __getattr__(self, item: str) -> Any:
        """
        Overrides the attribute getter to dynamically fetch values from `_config_data`.

        :param item: `str`
            The attribute name.

        :return: `Any`
            The fetched value.

        :raises:
            :raise AttributeError: If the attribute is not found in any of the registered configurations.
        """

        try:
            return self._get_value_from_config_data(item)
        except KeyError as error:
            raise AttributeError(f"Project config has no value for key '{item}'") from error

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Overrides the default `__setattr__` method to handle attribute assignments.
        Sets the specified attribute `key` to the provided value in the `_config_data`.

        :param key: `str`
            The attribute name.

        :param value: `Any`
            The value to be assigned to the attribute.
        """

        if key.startswith("_"):
            return super().__setattr__(key, value)

        self._config_data[key] = value

    def get(self, key: str, default: Any = MISSING) -> Any:
        """
        Takes information from specified config and return value if exists, otherwise return default

        :param key: `str`
            Attribute name

        :param default: `Any`
            (Optional) Default value that must be returned if key does not exist.
            By default, MISSING

        :return: `Any`
            Value of attribute or default
        """

        try:
            return self.__getattr__(key)
        except AttributeError:
            return default

    def register_config(self, config: AbstractConfig) -> None:
        """
        Loads and registers config values to the project config

        :param config: `AbstractConfig`
            The configuration instance.
        """

        self._config_data.update(config.load())

    def setup_from_environment(self) -> None:
        """
        Sets up PyModuleConfig based on the specified environment variable.

        :raises:
            :raise ConfigurationError: If the environment variable is not defined.
        """

        settings_module = os.environ.get(self.__class__.ENVIRONMENT_VARIABLE)

        if not settings_module:
            raise ConfigurationError(
                "Requested settings, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call project_config.set_config() before accessing settings."
                % self.__class__.ENVIRONMENT_VARIABLE
            )

        self.register_config(PyModuleConfig(settings_module))


project_settings = ProjectSettings()
