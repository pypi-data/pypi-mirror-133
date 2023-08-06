from __future__ import annotations
from typing import Dict, Any, Tuple


class ItemBase:
    _seeds: Dict[str, Any]
    _steps: Dict[str, Any]


class AttrBase:
    def __set_name__(self, obj: Any, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name})"


class SeedBase(AttrBase):
    """SeedBase"""


class StepBase(AttrBase):
    func: Any
    args: Tuple[Any, ...]
    kwargs: Dict[Any, Any]
