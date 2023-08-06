from typing import Union, Tuple, Dict, Any

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


# ### Render ###
RendererExtra = Any
"""
A rendering extra can provide additional functionality, such as backlight or contrast control
"""
RendererExtras = Dict[str, Any]
"""
A dictionary of RenderingExtra.
It is recommended to provide the user with key constants to access rendering extras via a RenderTarget
"""
