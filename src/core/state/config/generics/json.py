import json
from typing import Any, Dict

from src.core.state.config.abc import AbstractConfig
from src.core.utils.collections import DotDict


class JsonFileConfig(AbstractConfig):
    """
    Represents a configuration class that uses a JSON file for storing settings.
    Note: File will not be modified during settings update

    Methods:
    - `__init__(self, path: str) -> None`
        Initializes the JsonFileConfig instance

    - `load(self) -> Dict[str, Any]`
         Load data from the specified JSON file.
    """

    def __init__(self, path: str, use_dotdict: bool = True) -> None:
        """
        Initializes the JsonFileConfig instance by loading data from the specified JSON file.

        :param path: `str`
            The path to the JSON file.

        :param use_dotdict: `bool`
            If True, json will be converted to DotDict
        """

        self._file_path = path
        self._use_dotdict = use_dotdict

    def load(self) -> Dict[str, Any]:
        """
        Loads and returns configuration data from the specified JSON file.

        :return: `Dict[str, Any]`
            A dictionary containing configuration data.
        """

        with open(self._file_path, "r") as file:
            data = json.load(file)

            if self._use_dotdict:
                data = DotDict(init_data=data)

            return data
