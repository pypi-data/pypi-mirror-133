#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2019-2022 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
# *****************************************************************************
""" Builtin decoders using the base elements. """

from typing import Union as _Union

from .angles import Angle as _Angle
from .decoders import (
    MetaColorDecoder as _MetaColorDecoder,
    alias as _alias, fallback as _fallback,
)
from .colors import (
    CMYKColor as _CMYKColor, Color as _Color, HSLColor as _HSLColor,
    HSVColor as _HSVColor, HWBColor as _HWBColor, LABColor as _LABColor,
    LCHColor as _LCHColor, SRGBColor as _SRGBColor, XYZColor as _XYZColor,
    YIQColor as _YIQColor, YUVColor as _YUVColor,
)
from .utils import factor as _factor

__all__ = [
    'CSS1ColorDecoder', 'CSS2ColorDecoder', 'CSS3ColorDecoder',
    'CSS4ColorDecoder', 'DefaultColorDecoder',
]

_number = _Union[int, float]


def _rgb(x):
    """ Return an RGB color out of the given 6-digit hexadecimal code. """

    from thcolor.colors import SRGBColor as _SRGBColor

    return _SRGBColor(
        int(x[1:3], 16) / 255,
        int(x[3:5], 16) / 255,
        int(x[5:7], 16) / 255,
    )


# ---
# Main colors.
# ---


class CSS1ColorDecoder(_MetaColorDecoder):
    """ Named colors from CSS Level 1.

        See `<https://www.w3.org/TR/CSS1/>`_ for more information.
    """

    black = _rgb('#000000')
    silver = _rgb('#c0c0c0')
    gray = _rgb('#808080')
    white = _rgb('#ffffff')

    maroon = _rgb('#800000')
    red = _rgb('#ff0000')
    purple = _rgb('#800080')
    fuchsia = _rgb('#ff00ff')
    green = _rgb('#008000')
    lime = _rgb('#00ff00')
    olive = _rgb('#808000')
    yellow = _rgb('#ffff00')
    navy = _rgb('#000080')
    blue = _rgb('#0000ff')
    teal = _rgb('#008080')
    aqua = _rgb('#00ffff')

    transparent = _SRGBColor(0, 0, 0, 0)

    def rgb(red: int = 0, green: int = 0, blue: int = 0) -> _Color:
        """ Make an RGB color out of the given components. """

        return _SRGBColor(
            red=_factor(red, max_=255, clip=True),
            green=_factor(green, max_=255, clip=True),
            blue=_factor(blue, max_=255, clip=True),
            alpha=1.0,
        )


class CSS2ColorDecoder(CSS1ColorDecoder):
    """ Named colors from CSS Level 2 (Revision 1).

        See `<https://www.w3.org/TR/CSS2/>`_ for more information.
    """

    orange = _rgb('#ffa500')


class CSS3ColorDecoder(CSS2ColorDecoder):
    """ Named colors and functions from CSS Color Module Level 3.

        See `<https://drafts.csswg.org/css-color-3/>`_ for more information.
    """

    darkblue = _rgb('#00008B')
    mediumblue = _rgb('#0000CD')
    darkgreen = _rgb('#006400')
    darkcyan = _rgb('#008B8B')
    deepskyblue = _rgb('#00BFFF')
    darkturquoise = _rgb('#00CED1')
    mediumspringgreen = _rgb('#00FA9A')
    springgreen = _rgb('#00FF7F')
    cyan = _rgb('#00FFFF')
    midnightblue = _rgb('#191970')
    dodgerblue = _rgb('#1E90FF')
    lightseagreen = _rgb('#20B2AA')
    forestgreen = _rgb('#228B22')
    seagreen = _rgb('#2E8B57')
    darkslategray = _rgb('#2F4F4F')
    darkslategrey = _rgb('#2F4F4F')
    limegreen = _rgb('#32CD32')
    mediumseagreen = _rgb('#3CB371')
    turquoise = _rgb('#40E0D0')
    royalblue = _rgb('#4169E1')
    steelblue = _rgb('#4682B4')
    darkslateblue = _rgb('#483D8B')
    mediumturquoise = _rgb('#48D1CC')
    indigo = _rgb('#4B0082')
    darkolivegreen = _rgb('#556B2F')
    cadetblue = _rgb('#5F9EA0')
    cornflowerblue = _rgb('#6495ED')
    mediumaquamarine = _rgb('#66CDAA')
    dimgray = _rgb('#696969')
    dimgrey = _rgb('#696969')
    slateblue = _rgb('#6A5ACD')
    olivedrab = _rgb('#6B8E23')
    slategray = _rgb('#708090')
    slategrey = _rgb('#708090')
    lightslategray = _rgb('#778899')
    lightslategrey = _rgb('#778899')
    mediumslateblue = _rgb('#7B68EE')
    lawngreen = _rgb('#7CFC00')
    chartreuse = _rgb('#7FFF00')
    aquamarine = _rgb('#7FFFD4')
    grey = _rgb('#808080')
    skyblue = _rgb('#87CEEB')
    lightskyblue = _rgb('#87CEFA')
    blueviolet = _rgb('#8A2BE2')
    darkred = _rgb('#8B0000')
    darkmagenta = _rgb('#8B008B')
    saddlebrown = _rgb('#8B4513')
    darkseagreen = _rgb('#8FBC8F')
    lightgreen = _rgb('#90EE90')
    mediumpurple = _rgb('#9370DB')
    darkviolet = _rgb('#9400D3')
    palegreen = _rgb('#98FB98')
    darkorchid = _rgb('#9932CC')
    yellowgreen = _rgb('#9ACD32')
    sienna = _rgb('#A0522D')
    brown = _rgb('#A52A2A')
    darkgray = _rgb('#A9A9A9')
    darkgrey = _rgb('#A9A9A9')
    lightblue = _rgb('#ADD8E6')
    greenyellow = _rgb('#ADFF2F')
    paleturquoise = _rgb('#AFEEEE')
    lightsteelblue = _rgb('#B0C4DE')
    powderblue = _rgb('#B0E0E6')
    firebrick = _rgb('#B22222')
    darkgoldenrod = _rgb('#B8860B')
    mediumorchid = _rgb('#BA55D3')
    rosybrown = _rgb('#BC8F8F')
    darkkhaki = _rgb('#BDB76B')
    mediumvioletred = _rgb('#C71585')
    indianred = _rgb('#CD5C5C')
    peru = _rgb('#CD853F')
    chocolate = _rgb('#D2691E')
    tan = _rgb('#D2B48C')
    lightgray = _rgb('#D3D3D3')
    lightgrey = _rgb('#D3D3D3')
    thistle = _rgb('#D8BFD8')
    orchid = _rgb('#DA70D6')
    goldenrod = _rgb('#DAA520')
    palevioletred = _rgb('#DB7093')
    crimson = _rgb('#DC143C')
    gainsboro = _rgb('#DCDCDC')
    plum = _rgb('#DDA0DD')
    burlywood = _rgb('#DEB887')
    lightcyan = _rgb('#E0FFFF')
    lavender = _rgb('#E6E6FA')
    darksalmon = _rgb('#E9967A')
    violet = _rgb('#EE82EE')
    palegoldenrod = _rgb('#EEE8AA')
    lightcoral = _rgb('#F08080')
    khaki = _rgb('#F0E68C')
    aliceblue = _rgb('#F0F8FF')
    honeydew = _rgb('#F0FFF0')
    azure = _rgb('#F0FFFF')
    sandybrown = _rgb('#F4A460')
    wheat = _rgb('#F5DEB3')
    beige = _rgb('#F5F5DC')
    whitesmoke = _rgb('#F5F5F5')
    mintcream = _rgb('#F5FFFA')
    ghostwhite = _rgb('#F8F8FF')
    salmon = _rgb('#FA8072')
    antiquewhite = _rgb('#FAEBD7')
    linen = _rgb('#FAF0E6')
    lightgoldenrodyellow = _rgb('#FAFAD2')
    oldlace = _rgb('#FDF5E6')
    magenta = _rgb('#FF00FF')
    deeppink = _rgb('#FF1493')
    orangered = _rgb('#FF4500')
    tomato = _rgb('#FF6347')
    hotpink = _rgb('#FF69B4')
    coral = _rgb('#FF7F50')
    darkorange = _rgb('#FF8C00')
    lightsalmon = _rgb('#FFA07A')
    lightpink = _rgb('#FFB6C1')
    pink = _rgb('#FFC0CB')
    gold = _rgb('#FFD700')
    peachpuff = _rgb('#FFDAB9')
    navajowhite = _rgb('#FFDEAD')
    moccasin = _rgb('#FFE4B5')
    bisque = _rgb('#FFE4C4')
    mistyrose = _rgb('#FFE4E1')
    blanchedalmond = _rgb('#FFEBCD')
    papayawhip = _rgb('#FFEFD5')
    lavenderblush = _rgb('#FFF0F5')
    seashell = _rgb('#FFF5EE')
    cornsilk = _rgb('#FFF8DC')
    lemonchiffon = _rgb('#FFFACD')
    floralwhite = _rgb('#FFFAF0')
    snow = _rgb('#FFFAFA')
    lightyellow = _rgb('#FFFFE0')
    ivory = _rgb('#FFFFF0')

    def rgb(
        red: _number = 0,
        green: _number = 0,
        blue: _number = 0,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an RGB color out of the given components. """

        return _SRGBColor(
            red=_factor(red, max_=255, clip=True),
            green=_factor(green, max_=255, clip=True),
            blue=_factor(blue, max_=255, clip=True),
            alpha=_factor(alpha, clip=True),
        )

    def hsl(
        hue: _Angle,
        saturation: _number,
        lightness: _number,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an HSL color out of the given components. """

        return _HSLColor(
            hue=hue,
            saturation=_factor(saturation),
            lightness=_factor(lightness),
            alpha=_factor(alpha),
        )

    rgba = _alias('rgb')
    hsla = _alias('hsl')


class CSS4ColorDecoder(CSS3ColorDecoder):
    """ Named colors and functions from CSS Color Module Level 4.

        See `<https://drafts.csswg.org/css-color/>`_ for more information..
    """

    __extended_hex_support__ = True

    rebeccapurple = _rgb('#663399')

    def hwb(
        hue: _Angle,
        whiteness: _number = 0.0,
        blackness: _number = 0.0,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an HWB color out of the given components. """

        return _HWBColor(
            hue=hue,
            whiteness=_factor(whiteness),
            blackness=_factor(blackness),
            alpha=_factor(alpha),
        )

    def gray(gray: _number, alpha: _number = 1.0) -> _Color:
        """ Make a gray-scale color out of the given components. """

        gray = _factor(gray, max_=255)
        return _SRGBColor(gray, gray, gray, _factor(alpha))

    def lab(
        light: _number,
        a: _number,
        b: _number,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an LAB color out of the given components. """

        return _LABColor(
            lightness=max(_factor(light), 0.0),
            a=a, b=b,
            alpha=_factor(alpha),
        )

    def lch(
        light: _number,
        chroma: _number,
        hue: _Angle,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an LCH color out of the given components. """

        return _LCHColor(
            light=max(_factor(light), 0.0),
            chroma=max(chroma, 0.0),
            hue=hue,
            alpha=_factor(alpha),
        )

    hwba = _alias('hwb')


class DefaultColorDecoder(CSS4ColorDecoder):
    """ Functions extending the CSS Color Module Level 4 reference. """

    __ncol_support__ = True

    rbg = _alias('rgb', args=('red', 'blue', 'green', 'alpha'))
    rbga = _alias('rgb', args=('red', 'blue', 'green', 'alpha'))
    brg = _alias('rgb', args=('blue', 'red', 'green', 'alpha'))
    brga = _alias('rgb', args=('blue', 'red', 'green', 'alpha'))
    bgr = _alias('rgb', args=('blue', 'green', 'red', 'alpha'))
    bgra = _alias('rgb', args=('blue', 'green', 'red', 'alpha'))
    gbr = _alias('rgb', args=('green', 'blue', 'red', 'alpha'))
    gbra = _alias('rgb', args=('green', 'blue', 'red', 'alpha'))
    grb = _alias('rgb', args=('green', 'red', 'blue', 'alpha'))
    grba = _alias('rgb', args=('green', 'red', 'blue', 'alpha'))
    hls = _alias('hsl', args=('hue', 'lightness', 'saturation', 'alpha'))
    hlsa = _alias('hsl', args=('hue', 'lightness', 'saturation', 'alpha'))
    hbw = _alias('hwb', args=('hue', 'blackness', 'whiteness', 'alpha'))
    hbwa = _alias('hwb', args=('hue', 'blackness', 'whiteness', 'alpha'))
    device_cmyk = _alias('cmyk')

    def cmyk(
        cyan: _number,
        magenta: _number = 0.0,
        yellow: _number = 0.0,
        black: _number = 0.0,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make a CMYK color out of the given components. """

        return _CMYKColor(
            cyan=_factor(cyan),
            magenta=_factor(magenta),
            yellow=_factor(yellow),
            black=_factor(black),
            alpha=_factor(alpha),
        )

    def hsv(
        hue: _Angle,
        saturation: _number,
        value: _number,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an HSV color out of the given components. """

        return _HSVColor(
            hue=hue,
            saturation=_factor(saturation),
            value=_factor(value),
            alpha=_factor(alpha),
        )

    def xyz(
        x: _number,
        y: _number,
        z: _number,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make an XYZ color out of the given components. """

        return _XYZColor(
            x=_factor(x),
            y=_factor(y),
            z=_factor(z),
            alpha=_factor(alpha),
        )

    def yiq(
        y: _number,
        i: _number,
        q: _number,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make a YIQ color out of the given components. """

        return _YIQColor(
            y=_factor(y),
            i=_factor(i),
            q=_factor(q),
            alpha=_factor(alpha),
        )

    def yuv(
        y: _number,
        u: _number,
        v: _number,
        alpha: _number = 1.0,
    ) -> _Color:
        """ Make a YUV color out of the given components. """

        return _YUVColor(
            y=_factor(y),
            u=_factor(u),
            v=_factor(v),
            alpha=_factor(alpha),
        )

    # ---
    # Get the RGB components of a color.
    # ---

    @_fallback(_rgb('#ff0000'))
    def red(color: _Color) -> int:
        """ Get the red channel value from an RGB color. """

        r, g, b, _ = color.assrgb()
        return r

    @_fallback(_rgb('#00ff00'))
    def green(color: _Color) -> int:
        """ Get the green channel value from an RGB color. """

        r, g, b, _ = color.assrgb()
        return g

    @_fallback(_rgb('#0000ff'))
    def blue(color: _Color) -> int:
        """ Get the blue channel value from an RGB color. """

        r, g, b, _ = color.ascolor().assrgb()
        return b

    # ---
    # Manage the lightness and saturation for HSL colors.
    # ---

    def darker(by: float, color: _Color) -> _Color:
        """ Make the color darker by a given factor.

            This is accomplished by calling
            :py:meth:`thcolor.colors.Color.darker`.
        """

        return color.darker(by)

    def lighter(by: float, color: _Color) -> _Color:
        """ Make the color lighter by a given factor.

            This is accomplished by calling
            :py:meth:`thcolor.colors.Color.lighter`.
        """

        return color.lighter(by)

    def desaturate(by: float, color: _Color) -> _Color:
        """ Desaturate the color by a given factor.

            This is accomplished by calling
            :py:meth:`thcolor.colors.Color.desaturate`.
        """

        return color.desaturate(by)

    def saturate(by: float, color: _Color) -> _Color:
        """ Saturate the color by a given factor.

            This is accomplished by calling
            :py:meth:`thcolor.colors.Color.saturate`.
        """

        return color.saturate(by)

    # ---
    # Others.
    # ---

    def ncol(color: _Color) -> _Color:
        """ Return a natural color (NCol).

            This method is actually compatibility with w3color.js.
            NCols are managed directly without the function, so
            the function just needs to return the color.
        """

        return color


# End of file.
