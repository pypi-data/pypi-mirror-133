import sys
from datetime import datetime
from typing import Union, List, Tuple

import pygame
from PIL import Image
from pygame.surface import SurfaceType

from aurora.base.render import AuroraRenderTarget
from aurora.types import TwoDimSize
from aurora.utils.env import has_env_flag


def _pil_image_to_surface(image: Image):
    return pygame.image.frombuffer(image.tobytes(),
                                   image.size,
                                   image.mode).convert()


def _render_debug_text(header: str, data: List[Tuple[str, str]]) -> str:
    header_len = len(header)
    s = '{}\n'.format(header)
    max_w1 = max(list(map(lambda l: len(l[0]), data)))
    max_w2 = max(list(map(lambda l: len(l[1]), data)))
    if max_w1 + max_w2 < header_len:
        max_w2 = header_len - max_w1
    for line in data:
        c1 = ('{:<' + str(max_w1) + '}').format(line[0])
        c2 = ('{:>' + str(max_w2) + '}').format(line[1])
        s = s + '{}{}\n'.format(c1, c2)
    return s


def _render_multiline_text(text: str,
                           surface: Union[pygame.Surface, SurfaceType],
                           font: pygame.font.Font):
    lines = text.split('\n')
    frames: list[Union[pygame.Surface, SurfaceType]] = list(map(lambda txt: font.render(txt, True, (0, 255, 0), (0, 0, 0, 128)), lines))
    width = max(list(map(lambda r: _get_rect_width(r), frames)))
    height = sum(list(map(lambda r: _get_rect_height(r), frames)))

    total_width = surface.get_rect()[2]

    i = 0
    for frame in frames:
        surface.blit(frame, (total_width - width, i))
        i = i + _get_rect_height(frame)


def _get_rect_width(frame: Union[pygame.Surface, SurfaceType]) -> float:
    return frame.get_rect()[2]


def _get_rect_height(frame: Union[pygame.Surface, SurfaceType]) -> float:
    return frame.get_rect()[3]


class PyGameRenderTarget(AuroraRenderTarget):
    def __init__(self,
                 size: TwoDimSize,
                 scale: int = 10):
        super().__init__()
        self._size: TwoDimSize = size
        self._scale: int = scale

        self._logger.info('Initializing PyGame ...')
        pygame.init()
        self._window = pygame.display.set_mode(self.target_size)
        self._clock = pygame.time.Clock()

        self._last_frame_t: float = 0
        self._last_frame_time: datetime = datetime.utcnow()

        self._show_debug_overlay: bool = has_env_flag('AURORA_SHOW_DEBUG')

        try:
            pygame.font.init()
        except NotImplementedError:
            self._font: pygame.font.Font = None

        self._font: pygame.font.Font = None
        try:
            self._font = pygame.font.SysFont('firamono', 12)
        except:
            self._logger.error('Failed to load font, reverting to default')
            self._font = pygame.font.SysFont(None, 12)

        pygame.display.set_caption('Aurora Local Render Window - F3: Overlay')

    @property
    def target_size(self) -> TwoDimSize:
        return self._size[0] * self._scale, self._size[1] * self._scale

    @property
    def screen_size(self) -> TwoDimSize:
        return self._size

    def render_image(self, image: Image, render_time: float):
        self._clock.tick()

        try:
            self._window.fill(0)
            surface = _pil_image_to_surface(image)
            surface = pygame.transform.scale(surface,
                                             self.target_size)
        except pygame.error:
            self._logger.info('Ending render process')
            sys.exit(0)

        if self._show_debug_overlay:
            self._render_debug_overlay(surface, render_time)

        self._window.blit(surface,
                          surface.get_rect(topleft=(0, 0)))
        pygame.display.flip()

    def _render_debug_overlay(self,
                              surface,
                              render_time: float):
        ticks = pygame.time.get_ticks()
        now = datetime.utcnow()

        data = [
            ('Ticks:', '{} t   '.format(ticks)),
            ('Frame Time:', '{:.1f} ms/f'.format(render_time * 1000)),
            ('Frame Time (vsync):', '{} t/f '.format(ticks - self._last_frame_t)),
            ('Frame Rate:', '{:.1f} FPS '.format(1 / ((now - self._last_frame_time).total_seconds())))
        ]
        _render_multiline_text(_render_debug_text(' --- [ Aurora Debug Output ] --- ', data),
                               surface,
                               self._font)

        self._last_frame_t = ticks
        self._last_frame_time = now

    def handle_input(self, key: int):
        if key == pygame.K_F3:
            self._show_debug_overlay = not self._show_debug_overlay
        elif key == pygame.K_ESCAPE:
            pygame.quit()
        # elif key == pygame.K_F1:
        #     self._show_debug_grid = not self._show_debug_grid
        # elif key == pygame.K_SPACE:
        #     self._show_pixel_grid = not self._show_pixel_grid

    def __str__(self) -> str:
        return 'render.PyGame'


