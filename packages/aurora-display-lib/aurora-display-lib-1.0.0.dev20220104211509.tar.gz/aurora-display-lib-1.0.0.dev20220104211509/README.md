# Aurora Display Library for Python
Aurora Display Library is a small display library built on top of PIL/Pillow.
It is intended to be used for building applications for LED/LCD displays, mostly targeted towards Raspberry Pis.

## Origin
This library was created out of a project of mine where a Raspberry Pi would
run an [RGB LED matrix display](https://www.adafruit.com/product/420). I noticed that
I was constantly writing the same code over and over again. It also started to
become more difficult to test apps since they always had to run on that Pi with
the display connected. Thus, abstraction happened and the code of what now is
"Aurora" was born.

## Core Features
- Abstracted Render Targets
- Abstracted Input Sources
- Utility functions for:
  - Loading and managing resources (like fonts, images or colors)
  - Placing text in other orientations (center and right aligned)

Other than that, PIL/Pillow is used for rendering, therefore everything that
PIL/Pillow supports is doable here as well.

## Included in the box
- **PyGame** Renderer and Input Source for local development
- **Null** Renderer and Input Source for testing without in- or output
- Demo applications found under `aurora.demoapps`

> If your output can work with PIL/Pillow, it is fairly easy to implement
> a renderer to output the screen buffer to it.

## Installation
### PIP
```shell
pip3 install aurora-display-lib
```

### From Source
```shell
git clone ${REPO}/aurora-display-lib && cd aurora-display-lib
python3 setup.py install
```

## Contribution
I would be happy to receive pull/merge requests from you for improvements.
Also feel free to report any renderers, input sources, etc. you've created
so they can be linked here.
