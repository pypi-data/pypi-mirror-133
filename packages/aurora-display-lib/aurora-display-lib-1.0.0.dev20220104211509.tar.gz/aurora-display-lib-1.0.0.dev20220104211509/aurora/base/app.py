import time
from typing import Optional

from PIL import Image, ImageDraw

from aurora.base.base import LoggingObject
from aurora.base.input import AuroraInputSource
from aurora.base.render import AuroraRenderTarget
from aurora.utils.color import ColorDict
from aurora.utils.font import FontDict
from aurora.utils.image import ImageDict


class AuroraApplication(LoggingObject):
    def __init__(self,
                 render_target: AuroraRenderTarget,
                 input_source: Optional[AuroraInputSource],
                 buffer: Image.Image = None,
                 limit_render_speed: bool = True,
                 frame_limit: float = 30):
        super().__init__(str(self))

        self._render_target: AuroraRenderTarget = render_target
        self._input_source: Optional[AuroraInputSource] = input_source

        self._colors: ColorDict = ColorDict()
        self._fonts: FontDict = FontDict()
        self._images: ImageDict = ImageDict()

        if limit_render_speed:
            self._max_render_time = 1 / frame_limit
        else:
            self._logger.info('Frame Limiter disabled!')
            self._max_render_time = -1

        self._clean_buffer: Image.Image = buffer \
            if buffer is not None \
            else Image.new('RGB', self._render_target.screen_size)
        self._buffer: Image.Image = self._clean_buffer.copy()

    def _init_render_target(self):
        self._logger.info('Initializing Render Target ...')
        self._render_target.init()

    def _setup(self):
        self._logger.info('Setting up app ...')
        if self.has_input_source:
            self._input_source.setup()

        self._load_resources()

    def _teardown(self):
        self._logger.info('Tearing down app ...')
        if self.has_input_source:
            self._input_source.teardown()

    def _load_resources(self):
        self._logger.info('Loading resources ...')

    def _clear_buffer(self):
        self._buffer = self._clean_buffer.copy()

    def _main_loop(self):
        t_start = time.time()

        if self.has_input_source:
            self._input_source.process(self._render_target)

        self._clear_buffer()

        draw = ImageDraw.ImageDraw(self._buffer)
        self._render(draw, t_start)
        render_time = time.time() - t_start
        self._copy_buffer_to_screen(render_time)

        if self._max_render_time > 0:
            if render_time > self._max_render_time:
                self._logger.warn('Render time was longer than expected (took %.3f sec, max %.3f sec)',
                                  render_time, self._max_render_time)
            else:
                sleeping_for = max(self._max_render_time - (time.time() - t_start), 0)
                time.sleep(sleeping_for)

    def _render(self, draw: ImageDraw.ImageDraw, t: float):
        raise NotImplementedError()

    def _copy_buffer_to_screen(self, render_time: float):
        self._render_target.render_image(self._buffer.copy(), render_time)

    def _handle_input(self, key: int):
        pass

    @property
    def input_source(self) -> AuroraInputSource:
        return self._input_source

    @property
    def has_input_source(self):
        return self._input_source is not None

    def run(self):
        self._init_render_target()
        try:
            self._setup()
            while True:
                self._main_loop()
        except KeyboardInterrupt:
            self._logger.info('User has requested application to shut down (KeyboardInterrupt)')
        except SystemExit:
            self._logger.info('Raise System Exit, ending rendering process ...')

        self._teardown()

    def __str__(self) -> str:
        return 'AuroraApplication (not implemented!)'
