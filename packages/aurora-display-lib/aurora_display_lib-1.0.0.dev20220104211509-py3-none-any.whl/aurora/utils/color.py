from typing import Dict, Union

from aurora.types import AnyColor, RgbColor
from aurora.utils.dict_base import BaseUtilDict


def hex_to_rgb(hex_str: str) -> RgbColor:
    # noinspection PyTypeChecker
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


class ColorDict(BaseUtilDict):
    def __init__(self,
                 d: Dict[str, AnyColor] = None):
        super().__init__()
        self._dict: Dict[str, AnyColor] = {}
        if d:
            self.load_multiple(d)

    def get(self, key: str) -> AnyColor:
        return super().get(key)

    def set(self, key: str, value: AnyColor):
        super().set(key, value)

    def load_multiple(self, d: Dict[str, Union[str, AnyColor]]):
        for k, v in d.items():
            if type(v) == str:
                self.set(k, hex_to_rgb(v))
            else:
                self.set(k, v)

    def __str__(self) -> str:
        return 'util.Colors'


DEFAULT_COLORS = {
    'black': '000000',
    'white': 'ffffff',
    'red': 'ff0000',
    'green': '00ff00',
    'blue': '0000ff',
    'yellow': 'ffff00',
    'magenta': 'ff00ff',
    'aqua': '00ffff'
}
"""
A set of colors that get provided by default
when using get_default_color_dict().
"""


def get_default_color_dict() -> ColorDict:
    d = ColorDict()
    d.load_multiple(DEFAULT_COLORS)
    return d
