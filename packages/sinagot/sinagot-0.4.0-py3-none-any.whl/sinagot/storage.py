from __future__ import annotations
from typing import Union, Any, Dict, Type, Optional
from pathlib import Path
import os

import pandas as pd

from sinagot.base import AttrBase
from sinagot.logger import get_logger

logger = get_logger()


class LocalStorage(AttrBase):
    def __init__(
        self,
        path: Union[str, Path],
        read_kwargs: Optional[Dict[str, Any]] = None,
        write_kwargs: Optional[Dict[str, Any]] = None,
    ):
        self.path = path
        self.read_kwargs = read_kwargs or {}
        self.write_kwargs = write_kwargs or {}

    def __fspath__(self) -> str:
        return os.fspath(self.path)


class Storage:
    def __init__(
        self,
        path: Path,
        data_type: Any,
        read_kwargs: Dict[str, Any],
        write_kwargs: Dict[str, Any],
    ):
        self.path = path
        self.data_type = data_type
        self.format = self.path.suffix
        self.read_kwargs = read_kwargs
        self.write_kwargs = write_kwargs

    def _get_handler(self) -> TypeHandler:
        try:
            return type_handlers[self.data_type](
                read_kwargs=self.read_kwargs, write_kwargs=self.write_kwargs
            )
        except KeyError:
            raise NotImplementedError(f"{self.data_type.__name__} not implemented")

    def exists(self) -> bool:
        return self.path.exists()

    def read(
        self,
    ) -> Any:
        return self._get_handler().read(self.path)

    def write(self, data: Any) -> None:
        self._get_handler().write(self.path, data)


type_handlers: Dict[Any, Type[TypeHandler]] = {}


class TypeHandler:
    def __init_subclass__(cls, data_type: Any) -> None:
        type_handlers[data_type] = cls

    def __init__(
        self,
        read_kwargs: Dict[str, Any],
        write_kwargs: Dict[str, Any],
    ):
        self.read_kwargs = read_kwargs
        self.write_kwargs = write_kwargs

    def read(self, path: Path) -> Any:
        """read"""

    def write(self, path: Path, data: Any) -> None:
        """write"""


class StringHandler(TypeHandler, data_type=str):
    def read(self, path: Path) -> Any:
        return path.read_text(**self.read_kwargs)

    def write(self, path: Path, data: Any) -> None:
        path.write_text(data, **self.write_kwargs)


class IntHandler(TypeHandler, data_type=int):
    def read(self, path: Path) -> Any:
        return int(path.read_text(**self.read_kwargs))

    def write(self, path: Path, data: Any) -> None:
        path.write_text(str(data), **self.write_kwargs)


class DataFrameHandler(TypeHandler, data_type=pd.DataFrame):
    def read(self, path: Path) -> Any:
        return pd.read_csv(path, **self.read_kwargs)

    def write(self, path: Path, data: Any) -> None:
        data.to_csv(path, **self.write_kwargs)
