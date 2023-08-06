from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

from aurora.base.app import AuroraApplication
from aurora.base.input import NullInputSource, AuroraInputSource
from aurora.base.render import AuroraRenderTarget
from aurora.utils.color import DEFAULT_COLORS
from aurora.utils.font import FONT_TTF, draw_right_align_text


class ImageDemoApp(AuroraApplication):
    def __init__(self,
                 render_target: AuroraRenderTarget,
                 input_source: AuroraInputSource):
        super().__init__(render_target, input_source)

    def _load_resources(self):
        super()._load_resources()
        self._colors.load_multiple(DEFAULT_COLORS)

        self._fonts.load_font('OpenSans20', './res/fonts/OpenSans-Regular.ttf',
                              font_type=FONT_TTF,
                              font_size=20)

        self._images.load_image('bridge_orig', './res/imgs/mc_bridge.png')

        # Convert Image
        self._images.set('bridge_orig', self._images.get('bridge_orig').convert('RGB'))

        # Resize Images
        bridge = self._images.get('bridge_orig').resize((225, 225))
        self._images.set('bridge', bridge)

    def _render(self, draw: ImageDraw, t: float):
        # Background Text
        draw.text((10, 10),
                  ' *** AURORA IMAGE DEMO *** AURORA IMAGE DEMO *** ',
                  fill=self._colors.get('white'),
                  font=self._fonts.get('OpenSans20'))

        # Draw Original Image
        self._buffer.paste(self._images.get('bridge_orig'), box=(40, 40))
        draw_right_align_text(draw,
                              (475, 50),
                              'Original Size',
                              fill=self._colors.get('yellow'),
                              font=self._fonts.get('OpenSans20'))

        # Draw Resized Image
        self._buffer.paste(self._images.get('bridge'), box=(10, 10))
        draw.text((25, 20),
                  'Resized to {}'.format(self._images.get('bridge').size),
                  fill=self._colors.get('yellow'),
                  font=self._fonts.get('OpenSans20'))

        # Draw Moving Text
        p = (t % 5) / 5 * 500
        draw.text((p, p), 'Moving Text',
                  fill=self._colors.get('red'))
        draw_right_align_text(draw,
                              (500 - p, p),
                              'Moving Text',
                              fill=self._colors.get('green'))

    def __str__(self):
        return 'ImageDemoApp'
