from PIL import Image

from aurora.base.base import LoggingObject
from aurora.types import TwoDimSize, RendererExtras


class AuroraRenderTarget(LoggingObject):
    """
    Base implementation of a target (device, file or otherwise) to render an image on.
    When provided an image, this object is expected to render this image on whatever
    surface its target is.
    """
    def __init__(self):
        super().__init__(str(self))

    def init(self):
        """
        Initializes the render target.
        If your render target does not require any initialization, feel free to skip this.
        :return:
        """
        pass

    def render_image(self, image: Image, render_time: float):
        """
        Required rendering implementation
        :param image: The image to render
        :param render_time: The time in epoc seconds when the image started rendering
        :return:
        """
        raise NotImplementedError()

    def handle_input(self, key: int):
        """
        Handle special input keys, usually not required.
        Note: For example the PyGame implementation uses this to inject keys for enabling debug overviews
        or terminating the pygame process.
        :param key:
        :return:
        """
        pass

    @property
    def screen_size(self) -> TwoDimSize:
        """
        Returns the size of the screen to be rendered on
        :return: Tuple of width and height
        """
        raise NotImplementedError()

    @property
    def extras(self) -> RendererExtras:
        """
        Returns a list of dictionary of available extras
        :return:
        """
        return {}

    def has_extra(self, extra: str) -> bool:
        """
        Returns true if a specific extra is available
        :param extra: Extra key
        :return:
        """
        return extra in self.extras

    def __str__(self) -> str:
        return 'Aurora Render Target (not implemented)'


class NullRenderTarget(AuroraRenderTarget):
    """
    A target that doesn't render an image.
    Useful for testing.
    """
    def __init__(self,
                 screen_size: TwoDimSize = (100, 100)):
        super().__init__()
        self._screen_size = screen_size

    def init(self):
        super().init()

    def render_image(self, image: Image, render_time: float):
        pass

    @property
    def screen_size(self) -> TwoDimSize:
        return self._screen_size

    def __str__(self) -> str:
        return 'Null Render Target'
