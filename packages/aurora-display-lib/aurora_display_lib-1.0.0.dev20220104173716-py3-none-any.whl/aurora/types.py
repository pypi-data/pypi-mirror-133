from typing import Union, Tuple


# ### Color ### #
from PIL.ImageFont import ImageFont, FreeTypeFont

BinaryColor = int
RgbColor = Tuple[int, int, int]
RgbaColor = Tuple[int, int, int, int]

AnyColor = Union[BinaryColor, RgbColor, RgbaColor]


# ### Dimensions ###
TwoDimSize = Tuple[int, int]
TwoDimCoordinate = Tuple[int, int]


# ### Fonts ###
AnyFont = Union[ImageFont, FreeTypeFont]
