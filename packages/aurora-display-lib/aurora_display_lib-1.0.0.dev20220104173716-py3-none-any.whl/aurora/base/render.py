from PIL import Image

from aurora.base.base import LoggingObject
from aurora.types import TwoDimSize


class AuroraRenderTarget(LoggingObject):
    def __init__(self):
        super().__init__(str(self))

    def init(self):
        pass

    def render_image(self, image: Image, render_time: float):
        raise NotImplementedError()

    def handle_input(self, key: int):
        pass

    @property
    def screen_size(self) -> TwoDimSize:
        raise NotImplementedError()

    def __str__(self) -> str:
        return 'Aurora Render Target (not implemented)'


class NullRenderTarget(AuroraRenderTarget):
    def __init__(self):
        super().__init__()

    def init(self):
        super().init()

    def render_image(self, image: Image, render_time: float):
        pass

    @property
    def screen_size(self) -> TwoDimSize:
        return 100, 100

    def __str__(self) -> str:
        return 'Null Render Target'
