import os.path
from typing import Dict, Optional, Union, Tuple

from PIL import ImageFont
from PIL.BdfFontFile import BdfFontFile
from PIL.ImageDraw import ImageDraw

from aurora.types import AnyFont
from aurora.utils.base import has_flag
from aurora.utils.dict_base import BaseUtilDict

FontParams = Union[str, Tuple[str, int, int]]


FONT_RAW = 0b0001
FONT_TTF = 0b0010
FONT_BDF = 0b0100


def convert_bdf_to_pil_font(src_file: str,
                            pil_file: str):
    with open(src_file, 'rb') as fp:
        p = BdfFontFile(fp)
        p.save(pil_file)


class FontDict(BaseUtilDict):
    def __init__(self):
        super().__init__()
        self._dict: Dict[str, AnyFont] = {}

    def load_font(self,
                  key: str,
                  font_file: str,
                  font_type: int = FONT_RAW,
                  font_size: int = 10,
                  font_index: int = 0):
        font: Optional[AnyFont] = None
        if has_flag(font_type, FONT_RAW):
            self._logger.debug('Loading Raw font "%s" from "%s"',
                               key, font_file)
            font = ImageFont.load(font_file)
        elif has_flag(font_type, FONT_TTF):
            self._logger.debug('Loading TTF font "%s" from "%s"',
                               key, font_file)
            font = ImageFont.truetype(font_file,
                                      size=font_size,
                                      index=font_index)
        elif has_flag(font_type, FONT_BDF):
            pil_file = '{}.pil'.format(font_file)
            if not os.path.isfile(pil_file):
                self._logger.info('Generating PIL font from BDF font from file "%s"',
                                  font_file)
                convert_bdf_to_pil_font(font_file, pil_file)

            self.load_font(key, pil_file, FONT_RAW)
        else:
            raise NotImplementedError('Cannot load font of the type defined')

        if font:
            self.set(key, font)

    def get(self, key: str) -> AnyFont:
        return super().get(key)

    def set(self, key: str, value: AnyFont):
        super().set(key, value)

    def load_multiple(self, d: Dict[str, FontParams]):
        for key, params in d.items():
            if type(params) is str:
                font_type = FONT_BDF if params.lower().endswith('.bdf') else FONT_RAW
                self.load_font(key, params, font_type)
            elif type(params) == tuple and len(params) == 3:
                path: str = params[0]
                font_size: int = params[1]
                font_index: int = params[2]
                self.load_font(key, path, FONT_TTF, font_size, font_index)
            else:
                self._logger.error('Cannot load file "%s" / "%s" automatically using load_multiple(). '
                                   'Load manually using load_font().',
                                   key, str(params))

    def __str__(self) -> str:
        return 'utils.Fonts'


def right_align_text(draw: ImageDraw,
                     anchor_pos: Tuple[int, int],
                     text: str,
                     font=None):
    size = draw.textsize(text, font=font)
    return anchor_pos[0] - size[0], anchor_pos[1]


def draw_right_align_text(draw: ImageDraw,
                          anchor_pos: Union[Tuple[int, int], Tuple[float, float]],
                          text: str,
                          font=None,
                          fill=(255, 255, 255)):
    pos = right_align_text(draw, anchor_pos, text, font)
    draw.text(pos, text, fill=fill, font=font)


def center_align_text(draw: ImageDraw,
                      area: Tuple[int, int, int, int],
                      text: str,
                      font=None):
    w_t,h_t = draw.textsize(text, font=font)
    w_a,h_a = area[2] - area[0], area[3] - area[1]

    return area[0] + ((w_a - w_t) / 2), area[1] + ((h_a - h_t) / 2)


def draw_center_align_text(draw: ImageDraw,
                           area: Union[Tuple[int, int, int, int], Tuple[float, float, float, float]],
                           text: str,
                           font=None,
                           fill=(255, 255, 255),
                           bg: Tuple[int, int, int] = None):
    pos = center_align_text(draw, area, text, font)
    if bg:
        draw.rectangle(area, bg)
    draw.text(pos, text, fill=fill, font=font)


