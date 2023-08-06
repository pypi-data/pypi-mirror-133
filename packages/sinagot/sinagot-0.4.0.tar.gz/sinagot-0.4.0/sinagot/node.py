from __future__ import annotations
from typing import Any, Union, Optional
from pathlib import Path
import inspect

import ray

from sinagot.item import Item
from sinagot.base import StepBase, SeedBase
from sinagot.logger import get_logger
from sinagot.storage import Storage

logger = get_logger()


class NodeMixin:
    name: str

    def get_storage(self, item: Item) -> Optional[Storage]:
        store_path = getattr(item.workspace, self.name, None)
        if store_path is not None:
            path = item._resolve_path(store_path)
            data_type = item.__annotations__[self.name]
            return Storage(
                path=path,
                data_type=data_type,
                read_kwargs=store_path.read_kwargs,
                write_kwargs=store_path.write_kwargs,
            )
        return None


class Step(StepBase, NodeMixin):
    def __init__(self, func: Any, *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.store_path: Union[None, Path] = None

    def __get__(self, item: Item, objtype: Any = None) -> Any:
        return self.get_data(item)

    def get_data(self, item: Item) -> ray.ObjectRef:

        storage = self.get_storage(item)
        if (storage is not None) and storage.exists():
            logger.info("Getting %s data for item %s from storage", self, item.item_id)
            return storage.read()
        else:
            logger.info("Processing %s data for item %s", self, item.item_id)
            func = self.func
            kwargs = {}
            parameters = inspect.signature(func).parameters
            if "item_id" in parameters:
                kwargs["item_id"] = item.item_id

            result = item._run(self, **kwargs)

            if storage is not None:
                logger.info("Saving %s data for item %s", self, item.item_id)
                storage.write(ray.get(result))  # type: ignore

            return ray.get(result)  # type: ignore


def step(func: Any) -> Any:
    def step(*args: Any, **kwargs: Any) -> Step:
        return Step(func, *args, **kwargs)

    func.step = step
    return func


class Seed(SeedBase, NodeMixin):
    def __get__(self, item: Item, objtype: Any = None) -> Any:
        return self.get_data(item)

    def get_data(self, item: Item) -> ray.ObjectRef:
        storage = self.get_storage(item)
        if storage is not None:
            logger.info("Getting %s data for item %s", self, item.item_id)
            return storage.read()


def seed() -> Any:
    return Seed()
