from __future__ import annotations
from pathlib import Path
from glob import glob
import re
from typing import (
    Iterator,
    Generator,
    Union,
    Type,
    Generic,
    TypeVar,
    Mapping,
)

from sinagot.base import ItemBase
from sinagot.path_template import PathTemplate
from sinagot.logger import get_logger
from sinagot.config import get_settings
from sinagot.ray import init_ray

logger = get_logger()

IT = TypeVar("IT", bound=ItemBase)


class Workspace(Generic[IT], Mapping[str, IT]):

    ITEM_RE = ".*"
    Item: Type[IT]

    def __init__(self, *root_path_segments: Union[str, Path]):
        self.root_path = Path(*root_path_segments)
        self.settings = get_settings()
        init_ray()
        if type(self) != Workspace:
            logger.info("%s initialized", str(self))
            logger.debug("%s config :  %s", str(self), self.settings)

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.root_path}')"

    @property
    def item_class(self) -> Type[IT]:
        return self.__orig_bases__[0]().__orig_class__.__args__[0]  # type: ignore

    def __getitem__(self, item_id: str) -> IT:
        return self.item_class(self, item_id)  # type: ignore

    def __iter__(self) -> Iterator[str]:
        yield from self._iter_item_ids()

    def _iter_item_ids(self) -> Generator[str, None, None]:
        item_ids = set()
        data = [
            self._resolve_path(getattr(self, name)) for name in self.item_class._seeds
        ]
        glob_patterns = [item.format(item_id="*") for item in data]
        re_patterns = [str(item.format(item_id=f"({self.ITEM_RE})")) for item in data]
        for glob_pattern, re_pattern in zip(glob_patterns, re_patterns):
            for file_str in glob(str(glob_pattern)):
                item_match = re.match(re_pattern, file_str)
                if item_match:
                    item_id = item_match.group(1)
                    if item_id not in item_ids:
                        item_ids.add(item_id)
                        yield item_id

    def __len__(self) -> int:
        return len(list(self._iter_item_ids()))

    def _resolve_path(self, path: Path, **kwargs: str) -> PathTemplate:
        return PathTemplate(self.root_path, path).format(**kwargs)
