from typing import Optional

from PIL import Image
from aurora.base.render import AuroraRenderTarget
from aurora.types import TwoDimSize

from rgbmatrix.core import RGBMatrix, RGBMatrixOptions


__version__ = '1.0.0-dev20220104211843'
__license__ = 'MIT'
__title__ = 'aurora-renderer-rgbmatrix'


class RgbMatrixRenderTarget(AuroraRenderTarget):
    """
    RgbMatrixRenderTarget is a render target for rpi-rgb-led-matrix
    allowing you to display images on a RGB LED Matrix Display
    """
    def __init__(self,
                 size: TwoDimSize,
                 rgb_options: Optional[RGBMatrixOptions] = None,
                 rgb_brightness: int = 100,
                 rgb_gpio_slowdown: int = 3,
                 rgb_hardware_mapping: str = 'adafruit-hat'):
        """
        Initializes a new RgbMatrixRenderTarget with the provided options

        Note: For all options labelled rgb_, refer to rpi-rgb-led-matrix documentation found here:
        https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python

        :param size: Dimensions of the device being rendered on (<px> x <px>)
        :param rgb_options: (optional) RGBMatrixOptions settings, will override any other parameters
        :param rgb_brightness: (optional) Brightness of the display
        :param rgb_gpio_slowdown: (optional) Slowdown of GPIO communication to stabilize image
        :param rgb_hardware_mapping: (optional) Mapping for hardware being used
        """
        super().__init__()
        self._screen_size = size

        self._matrix: Optional[RGBMatrix] = None
        self._canvas: Optional[RGBMatrix] = None

        if rgb_options:
            self._options: RGBMatrixOptions = rgb_options
        else:
            self._options: RGBMatrixOptions = RGBMatrixOptions()
            o = self._options
            o.gpio_slowdown = rgb_gpio_slowdown
            o.brightness = rgb_brightness
            o.hardware_mapping = rgb_hardware_mapping

    def init(self):
        super().init()
        self._matrix = RGBMatrix(options=self._options)
        self._canvas = self._matrix.CreateFrameCanvas()

    def render_image(self, image: Image, render_time: float):
        c: RGBMatrix = self._canvas
        c.SetImage(image)
        self._matrix.SwapOnVSync()

    @property
    def screen_size(self) -> TwoDimSize:
        return self._screen_size

    def __str__(self) -> str:
        return 'render.RGBMatrix'


