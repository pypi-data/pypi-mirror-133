from typing import Dict, Any

from PIL import Image

from aurora.utils.dict_base import BaseUtilDict


class ImageDict(BaseUtilDict):
    def __init__(self,
                 d: Dict[str, str] = None):
        super().__init__()
        self._dict: Dict[str, Image.Image] = {}
        if d:
            self.load_multiple(d)

    def load_image(self,
                   key: str,
                   image_path: str):
        self._logger.info('Loading image "%s" from "%s"', key, image_path)
        self.set(key, Image.open(image_path))

    def get(self, key: str) -> Image.Image:
        return super().get(key)

    def set(self, key: str, value: Image.Image):
        super().set(key, value)

    def load_multiple(self, d: Dict[str, str]):
        for key, path in d.items():
            self.load_image(key, path)

    def __str__(self) -> str:
        return 'utils.Images'
