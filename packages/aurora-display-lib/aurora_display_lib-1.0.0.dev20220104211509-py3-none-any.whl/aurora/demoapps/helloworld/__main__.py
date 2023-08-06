import datetime

from PIL import ImageDraw

from aurora.base.app import AuroraApplication
from aurora.base.render import AuroraRenderTarget
from aurora.base.input import AuroraInputSource
from aurora.log import configure_logging
from aurora.render.pygame import PyGameRenderTarget
from aurora.input.pygame import PyGameInputSource
from aurora.utils.color import DEFAULT_COLORS
from aurora.utils.font import FONT_TTF, FONT_BDF, draw_center_align_text


class DemoApp1(AuroraApplication):
    def __init__(self,
                 render_target: AuroraRenderTarget,
                 input_source: AuroraInputSource):
        super().__init__(render_target,
                         input_source)

    def _load_resources(self):
        super()._load_resources()
        self._colors.load_multiple(DEFAULT_COLORS)
        self._fonts.load_font('10x20', './res/fonts/10x20.bdf',
                              font_type=FONT_BDF)
        self._fonts.load_font('OpenSans20', './res/fonts/OpenSans-Regular.ttf',
                              font_type=FONT_TTF,
                              font_size=20)

    def _render(self, draw: ImageDraw.ImageDraw, t: float):
        draw.rectangle((0, 100, 250, 150),
                       fill=self._colors.get('green'))
        draw_center_align_text(draw,
                               (0, 100, 250, 150),
                               datetime.datetime.now().strftime('%Y/%m/%d\n%H:%M:%S'),
                               fill=self._colors.get('black'),
                               font=self._fonts.get('OpenSans20'))

    def __str__(self) -> str:
        return 'DemoApp1'


if __name__ == '__main__':
    configure_logging()
    app = DemoApp1(PyGameRenderTarget((250, 250), scale=2),
                   PyGameInputSource())
    app.run()
