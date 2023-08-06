from io import BytesIO
from os.path import isfile
from bs4 import BeautifulSoup as bs
from cairo import Context, FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL, SVGSurface

from .cairo import create_cairo_font_face_for_file


def text2path(
    text: str,
    font: str,
    font_size: int = 16,
    x: int = 0,
    y: int = 0,
    width: int = 1000,
    height: int = 1000
) -> str:
    """
    Converts text to SVG path
    """

    # Create file-like SVG object ..
    pathio = BytesIO()

    # .. from `text`
    with SVGSurface(pathio, width, height) as surface:
        # Create drawing
        ctx = Context(surface)

        # If font file was provided ..
        if isfile(font):
            # .. load it
            ctx.set_font_face(create_cairo_font_face_for_file(font))

        # .. otherwise ..
        else:
            # .. treat it as font title
            ctx.select_font_face(font, FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL)

        # Set font size
        ctx.set_font_size(font_size)

        # Fix `pycairo` being (sometimes) unable to convert (certain) integers
        if text.isdigit() and y == 0:
            y = 1

        # Get ready ..
        ctx.move_to(x, y)

        # .. DRAW!
        ctx.text_path(text)

        # Fill it
        ctx.fill()

    # Set pointer to beginning
    pathio.seek(0)

    # Fetch first path element ..
    path = bs(pathio.read(), 'lxml').find('path')

    # .. but fail if none present
    if not path:
        raise Exception('Cannot render text: "%s"' % text)

    # Extract path defintion
    return path['d']
