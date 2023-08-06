from typing import Dict, List

import pygame.event

from aurora.base.input import AuroraInputSource
from aurora.base.render import AuroraRenderTarget


_PYGAME_RENDER_KEYS: List[int] = [
    pygame.K_F1,
    pygame.K_F3,
    pygame.K_SPACE,
    pygame.K_ESCAPE
]


class PyGameInputSource(AuroraInputSource):
    def __init__(self, key_remap: Dict[int, int] = None):
        super().__init__()
        self._key_remap: Dict[int, int] = key_remap if key_remap else {}  # _DEFAULT_KEY_MAP

    def process(self, render_target: AuroraRenderTarget):
        self._handle_pygame_events(render_target)

    def _handle_pygame_events(self, render_target: AuroraRenderTarget):
        for e in pygame.event.get():
            if e.type == pygame.KEYUP:
                key = e.key
                if self._handle_special_keys(key, render_target):
                    continue
                if key in self._key_remap:
                    key = self._key_remap[key]
                self._emit_callback(key)

    def _handle_special_keys(self, key: int, render_target: AuroraRenderTarget) -> bool:
        if key in _PYGAME_RENDER_KEYS:
            render_target.handle_input(key)
            return True
        return False

    def __str__(self) -> str:
        return 'input.PyGame'
