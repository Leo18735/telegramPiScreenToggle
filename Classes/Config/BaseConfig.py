from __future__ import annotations

import abc
import inspect
import typing


class BaseConfig(abc.ABC):
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
        return self
