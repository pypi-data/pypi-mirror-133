from aurora.demoapps.imagedemo import ImageDemoApp
from aurora.input.pygame import PyGameInputSource
from aurora.log import configure_logging
from aurora.render.pygame import PyGameRenderTarget


if __name__ == '__main__':
    configure_logging()
    ImageDemoApp(PyGameRenderTarget((500, 500), scale=2),
                 PyGameInputSource()).run()
