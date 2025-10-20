from __future__ import annotations

import abc
import inspect
import threading
import typing


class BaseConfig(abc.ABC):
    _lock: threading.Lock = threading.Lock()

    @staticmethod
    def _custom_loader(obj: BaseConfig, key: str, value):
        method_name: str = f"_custom_{key}"
        if not hasattr(obj, method_name):
            return value
        method: typing.Callable = getattr(obj, method_name)
        if not inspect.isfunction(method):
            return value
        return method(value)

    def load_config(self, config: dict):
        for key, obj in self.__dict__.items():
            if key.startswith("_"):
                continue
            value = config.get(key)
            if isinstance(obj, BaseConfig):
                obj.load_config(value)
                continue
            setattr(self, key, self._custom_loader(self, key, value))

    def __getattribute__(self, name):
        if name in ("_lock", "__dict__", "__class__"):  # avoid recursion
            return object.__getattribute__(self, name)
        with object.__getattribute__(self, "_lock"):
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in ("_lock", "__dict__", "__class__"):
            object.__setattr__(self, name, value)
        else:
            with self._lock:
                object.__setattr__(self, name, value)
