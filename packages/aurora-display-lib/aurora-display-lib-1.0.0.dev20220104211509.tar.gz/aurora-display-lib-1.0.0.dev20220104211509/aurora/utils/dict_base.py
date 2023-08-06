from typing import Dict, Any

from aurora.base.base import LoggingObject


class BaseUtilDict(LoggingObject):
    def __init__(self,
                 d: Dict[str, Any] = None):
        super().__init__(str(self))
        self._dict: Dict[str, Any] = {}
        if d:
            self.load_multiple(d)

    def get(self, key: str) -> Any:
        return self._dict[key]

    def set(self, key: str, value: Any):
        self._logger.debug('Setting "%s" to "%s"', key, str(value))
        self._dict[key] = value

    def load_multiple(self, d: Dict[str, Any]):
        for k, v in d.items():
            self.set(k, v)

    def has(self, key: str) -> bool:
        return key in self._dict

    def __str__(self) -> str:
        return 'BaseUtilDict'
