#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2019-2022 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
# *****************************************************************************
""" Color representations and conversions. """

from math import (
    atan2 as _atan2, ceil as _ceil, cos as _cos, sin as _sin, sqrt as _sqrt,
)
from typing import (
    Any as _Any, Optional as _Optional, Tuple as _Tuple, Sequence as _Sequence,
)

from .angles import (
    Angle as _Angle, DegreesAngle as _DegreesAngle,
    RadiansAngle as _RadiansAngle, TurnsAngle as _TurnsAngle,
)
from .utils import round_half_up as _round_half_up

__all__ = [
    'CMYKColor', 'Color', 'HSLColor', 'HSVColor', 'HWBColor',
    'LABColor', 'LCHColor', 'SRGBColor', 'XYZColor',
    'YIQColor', 'YUVColor',
]


class Color:
    """ Class representing a color within thcolor.

        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_alpha')
    _params: _Sequence[str] = ()

    def __init__(self, alpha: float = 1.0):
        super().__init__()

        try:
            alpha = float(alpha)
        except (TypeError, ValueError):
            raise ValueError(f'alpha should be a float, is {alpha!r}')
        else:
            if alpha < 0 or alpha > 1:
                raise ValueError('alpha should be between 0.0 and 1.0')

        self._alpha = alpha

    def __repr__(self):
        params = (
            (key, getattr(self, key))
            for key in self._params + ('alpha',)
        )
        return (
            f'{self.__class__.__name__}('
            f'{", ".join(f"{key}={val!r}" for key, val in params)})'
        )

    def __eq__(self, other: _Any) -> bool:
        if not isinstance(other, Color):
            return False

        srgb = tuple(map(lambda x: round(x, 3), self.assrgb()))
        orgb = tuple(map(lambda x: round(x, 3), other.assrgb()))

        return srgb == orgb

    @property
    def alpha(self) -> float:
        """ The alpha component value.

            Represented as a float varying between 0.0 (invisible)
            and 1.0 (opaque).
        """

        return self._alpha

    @classmethod
    def fromtext(
        cls,
        expr: str,
        decoder: _Optional[_Any] = None,
    ) -> 'Color':
        """ Create a color from a string.

            :param expr: The expression to decode.
        """

        if decoder is None:
            from .builtin import DefaultColorDecoder

            decoder = DefaultColorDecoder()

        results = decoder.decode(expr, prefer_colors=True)

        if len(results) != 1 or not isinstance(results[0], cls):
            raise ValueError(
                f'result of expression was not an instance of {cls.__name__}: '
                f'single color: {results!r}',
            )

        return results[0]

    # ---
    # Conversions.
    # ---

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        raise NotImplementedError

    def ashsl(self) -> 'HSLColor':
        """ Get an HSLColor out of the current object. """

        return self.assrgb().ashsl()

    def ashsv(self) -> 'HSVColor':
        """ Get an HSVColor out of the current object. """

        return self.assrgb().ashsv()

    def ashwb(self) -> 'HWBColor':
        """ Get an HWBColor out of the current object. """

        return self.assrgb().ashwb()

    def ascmyk(self) -> 'CMYKColor':
        """ Get a CMYKColor out of the current object. """

        return self.assrgb().ascmyk()

    def aslab(self) -> 'LABColor':
        """ Get a LABColor out of the current object. """

        raise NotImplementedError

    def aslch(self) -> 'LCHColor':
        """ Get a LCHColor out of the current object. """

        raise NotImplementedError

    def asxyz(self) -> 'XYZColor':
        """ Get an XYZColor out of the current object. """

        raise NotImplementedError

    def asyiq(self) -> 'YIQColor':
        """ Get an YIQColor out of the current object. """

        return self.assrgb().asyiq()

    def asyuv(self) -> 'YUVColor':
        """ Get an YUVColor out of the current object. """

        return self.assrgb().asyuv()

    # ---
    # Operations on colors.
    # ---

    def replace(self, **properties) -> 'Color':
        """ Get the color with the given properties replaced.

            For changing the alpha on an RGB color:

            .. code-block:: python

                >>> SRGBColor(.1, .2, .3).replace(alpha=.5)
                ... SRGBColor(red=0.1, green=0.2, blue=0.3, alpha=0.5)

            For changing the lightness on an HSL color:

            .. code-block:: pycon

                >>> HSLColor(DegreesAngle(270), .5, 1).replace(lightness=.2)
                ... HSLColor(hue=DegreesAngle(degrees=270.0), saturation=0.5,
                ...          lightness=0.2, alpha=1.0)

            :param properties: Properties to change from the original
                               color.
        """

        params = {
            key: getattr(self, key)
            for key in (*self._params, 'alpha')
        }

        for key, value in properties.items():
            if key not in params:
                raise KeyError(
                    f'no such argument {key!r} in '
                    f'{self.__class__.__name__} parameters',
                )

            params[key] = value

        return type(self)(**params)

    def darker(self, by: float = 0.1) -> 'Color':
        """ Get a darker version of the given color.

            :param by: Percentage by which the color should be darker.
        """

        color = self.ashsl()
        return color.replace(lightness=max(color.lightness - by, 0.0))

    def lighter(self, by: float = 0.1) -> 'Color':
        """ Get a lighter version of the given color.

            :param by: Percentage by which the color should be lighter.
        """

        color = self.ashsl()
        return color.replace(lightness=min(color.lightness + by, 1.0))

    def desaturate(self, by: float = 0.1) -> 'Color':
        """ Get a less saturated version of the given color.

            :param by: Percentage by which the color should be
                       desaturated.
        """

        color = self.ashsl()
        return color.replace(saturation=max(color.saturation - by, 0.0))

    def saturate(self, by: float = 0.1) -> 'Color':
        """ Get a more saturated version of the given color.

            :param by: Percentage by which the color should be
                       saturated.
        """

        color = self.ashsl()
        return color.replace(saturation=min(color.saturation + by, 1.0))

    def css(self) -> _Sequence[str]:
        """ Get the CSS color descriptions.

            Includes older CSS specifications compatibility,
            as a sequence of strings.

            For example:

                >>> SRGBColor.frombytes(18, 52, 86, 0.82).css()
                ... ("#123456", "rgba(18, 52, 86, 82%)")
        """

        def _percent(prop):
            per = _round_half_up(prop, 4) * 100
            if per == int(per):
                per = int(per)
            return per

        def _deg(agl):
            return int(agl.asdegrees().degrees)

        def statements():
            # Start by yelling a #RRGGBB color, compatible with most
            # web browsers around the world, followed by the rgba()
            # notation if the alpha value isn't 1.0.

            a = _round_half_up(self.alpha, 3)

            try:
                rgb = self.assrgb()
            except NotImplementedError:
                pass
            else:
                r, g, b = rgb.asbytes()

                yield f'#{r:02X}{g:02X}{b:02X}'

                if a < 1.0:
                    yield f'rgba({r}, {g}, {b}, {_percent(a)}%)'

            # Then yield more specific CSS declarations in case
            # they're supported (which would be neat!).

            if isinstance(self, HSLColor):
                hue, sat, lgt = (
                    self.hue, self.saturation, self.lightness,
                )
                args = (
                    f'{_deg(hue)}deg, {_percent(sat)}%, {_percent(lgt)}%'
                )

                if a < 1.0:
                    yield f'hsla({args}, {_percent(a)}%)'
                else:
                    yield f'hsl({args})'
            elif isinstance(self, HWBColor):
                hue, wht, blk = (
                    self.hue, self.whiteness, self.blackness)

                args = f'{_deg(hue)}deg, ' \
                    f'{_percent(wht)}%, {_percent(blk)}%'

                if a < 1.0:
                    yield f'hwba({args}, {_percent(a)}%)'
                else:
                    yield f'hwb({args})'

        return tuple(statements())

# ---
# Color implementations.
# ---


class SRGBColor(Color):
    """ A color expressed using its channel intensities in the sRGB profile.

        :param red: Value for :py:attr:`red`.
        :param green: Value for :py:attr:`green`.
        :param blue: Value for :py:attr:`blue`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_red', '_green', '_blue')
    _params = ('red', 'green', 'blue')

    def __init__(
        self,
        red: float,
        green: float,
        blue: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        try:
            red = float(red)
        except (TypeError, ValueError):
            raise ValueError(f'red should be a float, is {red!r}')
        else:
            if red < 0 or red > 1:
                raise ValueError('red should be between 0.0 and 1.0')

        try:
            green = float(green)
        except (TypeError, ValueError):
            raise ValueError(f'green should be a float, is {green!r}')
        else:
            if green < 0 or green > 1:
                raise ValueError('green should be between 0.0 and 1.0')

        try:
            blue = float(blue)
        except (TypeError, ValueError):
            raise ValueError(f'blue should be a float, is {blue!r}')
        else:
            if blue < 0 or blue > 1:
                raise ValueError('blue should be between 0.0 and 1.0')

        self._red = red
        self._green = green
        self._blue = blue

    def __iter__(self):
        return iter((
            self.red,
            self.green,
            self.blue,
            self.alpha,
        ))

    @property
    def red(self) -> float:
        """ The intensity of the red channel.

            Represented as a float between 0.0 (dark) and 1.0 (light).
        """

        return self._red

    @property
    def green(self) -> float:
        """ The intensity of the green channel.

            Represented as a float between 0.0 (dark) and 1.0 (light).
        """

        return self._green

    @property
    def blue(self) -> float:
        """ The intensity of the blue channel.

            Represented as a float between 0.0 (dark) and 1.0 (light).
        """

        return self._blue

    @classmethod
    def frombytes(
        cls,
        red: int,
        green: int,
        blue: int,
        alpha: float = 1.0,
    ) -> 'SRGBColor':
        """ Get an sRGB color from colors using values between 0 and 255. """

        return cls(
            red=red / 255,
            green=green / 255,
            blue=blue / 255,
            alpha=alpha,
        )

    @classmethod
    def fromnetscapecolorname(cls, name: str) -> 'SRGBColor':
        """ Get an sRGB color from a Netscape color name. """

        name = str(name)
        if name[0] == '#':
            name = name[1:]

        # Find more about this here: https://stackoverflow.com/a/8333464
        #
        # First of all:
        # - we sanitize our input by replacing invalid characters
        #   by '0' characters (the 0xFFFF limit is due to how
        #   UTF-16 was managed at the time).
        # - we truncate our input to 128 characters.

        name = name.lower()
        name = ''.join(
            c if c in '0123456789abcdef' else '00'[:1 + (ord(c) > 0xFFFF)]
            for c in name[:128]
        )[:128]

        # Then we calculate some values we're going to need.
        # `iv` is the size of the zone for a member.
        # `sz` is the size of the digits slice to take in that zone
        # (max. 8).
        # `of` is the offset in the zone of the slice to take.

        iv = _ceil(len(name) / 3)
        of = iv - 8 if iv > 8 else 0
        sz = iv - of

        # Then we isolate the slices using the values calculated
        # above. `gr` will be an array of 3 or 4 digit strings
        # (depending on the number of members).

        gr = list(map(
            lambda i: name[i * iv + of:i * iv + iv].ljust(sz, '0'),
            range(3),
        ))

        # Check how many digits we can skip at the beginning of
        # each slice.

        pre = min(map(lambda x: len(x) - len(x.lstrip('0')), gr))
        pre = min(pre, sz - 2)

        # Then we extract the values.

        r, g, b = map(lambda x: int('0' + x[pre:pre + 2], 16), gr)

        return cls.frombytes(r, g, b)

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        return SRGBColor(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha,
        )

    def ashsl(self) -> 'HSLColor':
        """ Get an HSLColor out of the current object. """

        r, g, b = self.red, self.green, self.blue

        min_value = min((r, g, b))
        max_value = max((r, g, b))
        chroma = max_value - min_value

        if chroma == 0:
            hue = 0.
        elif r == max_value:
            hue = (g - b) / chroma
        elif g == max_value:
            hue = (b - r) / chroma + 2
        else:
            hue = (r - g) / chroma + 4

        hue = hue * 60 + (hue < 0) * 360
        lgt = (min_value + max_value) / 2
        if min_value == max_value:
            s = 0.
        else:
            s = max_value - min_value
            if lgt < 0.5:
                s /= max_value + min_value
            else:
                s /= 2 - max_value - min_value

        return HSLColor(
            hue=_DegreesAngle(_round_half_up(hue, 2)),
            saturation=_round_half_up(s, 2),
            lightness=_round_half_up(lgt, 2),
            alpha=self.alpha,
        )

    def ashsv(self) -> 'HSVColor':
        """ Get an HSVColor out of the current object. """

        r, g, b = self.red, self.green, self.blue
        maxc = max(r, g, b)
        minc = min(r, g, b)

        value = maxc
        if minc == maxc:
            turns, saturation = 0., 0.
        else:
            saturation = (maxc - minc) / maxc
            rc, gc, bc = map(lambda x: (maxc - x) / (maxc - minc), (r, g, b))

            if r == maxc:
                turns = bc - gc
            elif g == maxc:
                turns = 2 + rc - bc
            else:
                turns = 4 + gc - rc

            turns = (turns / 6) % 1

        return HSVColor(
            hue=_TurnsAngle(turns),
            saturation=saturation,
            value=value,
            alpha=self.alpha,
        )

    def ashwb(self) -> 'HWBColor':
        """ Get an HWBColor out of the current object. """

        r, g, b = self.red, self.green, self.blue

        max_ = max((r, g, b))
        min_ = min((r, g, b))
        chroma = max_ - min_

        if chroma == 0:
            hue = 0
        elif r == max_:
            hue = (g - b) / chroma
        elif g == max_:
            hue = (b - r) / chroma + 2
        elif b == max_:
            hue = (r - g) / chroma + 4

        hue /= 6
        w = min_
        b = 1 - max_

        return HWBColor(
            hue=_TurnsAngle(hue),
            whiteness=w,
            blackness=b,
            alpha=self.alpha,
        )

    def ascmyk(self) -> 'CMYKColor':
        """ Get a CMYKColor out of the current object. """

        r, g, b, _ = self

        k = 1 - max((r, g, b))
        if k == 1:
            c, m, y = 0, 0, 0
        else:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)

        return CMYKColor(
            cyan=c,
            magenta=m,
            yellow=y,
            black=k,
            alpha=self.alpha,
        )

    def asyiq(self) -> 'YIQColor':
        """ Get an YIQColor out of the current object. """

        r, g, b = self.red, self.green, self.blue
        y = .3 * r + .59 * g + .11 * b

        return YIQColor(
            y=y,
            i=.74 * (r - y) - .27 * (b - y),
            q=.48 * (r - y) + .41 * (b - y),
            alpha=self.alpha,
        )

    def asyuv(self) -> 'YUVColor':
        """ Get an YUVColor out of the current object. """

        raise NotImplementedError  # TODO

    def asbytes(self) -> _Tuple[int, int, int]:
        """ Get the red, blue and green bytes. """

        return (
            int(_round_half_up(self.red * 255)),
            int(_round_half_up(self.green * 255)),
            int(_round_half_up(self.blue * 255)),
        )


class HSLColor(Color):
    """ A color expressed using its hue, saturation and lightness components.

        :param hue: Value for :py:attr:`hue`.
        :param saturation: Value for :py:attr:`saturation`.
        :param lightness: Value for :py:attr:`lightness`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_hue', '_saturation', '_lightness')
    _params = ('hue', 'saturation', 'lightness')

    def __init__(
        self,
        hue: _Angle,
        saturation: float,
        lightness: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._hue = hue
        self._saturation = saturation
        self._lightness = lightness

    def __iter__(self):
        return iter((self.hue, self.saturation, self.lightness, self.alpha))

    @property
    def hue(self) -> _Angle:
        """ The hue, as an angle. """

        return self._hue

    @property
    def saturation(self) -> float:
        """ The saturation, between 0.0 and 1.0. """

        return self._saturation

    @property
    def lightness(self) -> float:
        """ The lightness, between 0.0 and 1.0. """

        return self._lightness

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        hue, s, lgt = self.hue.asdegrees(), self.saturation, self.lightness

        if s == 0:
            # Achromatic color.

            return SRGBColor(
                red=lgt,
                green=lgt,
                blue=lgt,
                alpha=self.alpha,
            )

        def _hue_to_rgb(t1, t2, hue):
            hue %= 6

            if hue < 1:
                return t1 + (t2 - t1) * hue
            elif hue < 3:
                return t2
            elif hue < 4:
                return t1 + (t2 - t1) * (4 - hue)
            return t1

        hue = (hue.degrees % 360) / 60
        if lgt <= 0.5:
            t2 = lgt * (s + 1)
        else:
            t2 = lgt + s - (lgt * s)

        t1 = lgt * 2 - t2

        return SRGBColor(
            red=_hue_to_rgb(t1, t2, hue + 2),
            green=_hue_to_rgb(t1, t2, hue),
            blue=_hue_to_rgb(t1, t2, hue - 2),
            alpha=self.alpha,
        )

    def ashsl(self) -> 'HSLColor':
        """ Get an HSLColor out of the current object. """

        return HSLColor(
            hue=self.hue,
            saturation=self.saturation,
            lightness=self.lightness,
            alpha=self.alpha,
        )


class HSVColor(Color):
    """ A color expressed using its hue, saturation and value components.

        :param hue: Value for :py:attr:`hue`.
        :param saturation: Value for :py:attr:`saturation`.
        :param value: Value for :py:attr:`value`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_hue', '_saturation', '_value')
    _params = ('hue', 'saturation', 'value')

    def __init__(
        self,
        hue: _Angle,
        saturation: float,
        value: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._hue = hue
        self._saturation = saturation
        self._value = value

    def __iter__(self):
        return iter((self.hue, self.saturation, self.value, self.alpha))

    @property
    def hue(self) -> _Angle:
        """ The hue, as an angle. """

        return self._hue

    @property
    def saturation(self) -> float:
        """ The saturation, between 0.0 and 1.0. """

        return self._saturation

    @property
    def value(self) -> float:
        """ The value, between 0.0 and 1.0. """

        return self._value

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        hue, saturation, value = (
            self.hue.asturns(),
            self.saturation,
            self.value,
        )

        if saturation == 0:
            r, g, b = value, value, value
        else:
            f = hue.turns * 6.0
            f, i = f - int(f), int(f) % 6

            p = value * (1.0 - saturation)
            q = value * (1.0 - saturation * f)
            t = value * (1.0 - saturation * (1.0 - f))

            if i == 0:
                r, g, b = value, t, p
            elif i == 1:
                r, g, b = q, value, p
            elif i == 2:
                r, g, b = p, value, t
            elif i == 3:
                r, g, b = p, q, value
            elif i == 4:
                r, g, b = t, p, value
            elif i == 5:
                r, g, b = value, p, q

        return SRGBColor(
            red=r,
            green=g,
            blue=b,
            alpha=self.alpha,
        )

    def ashsv(self) -> 'HSVColor':
        """ Get an HSVColor out of the current object. """

        return HSVColor(
            hue=self.hue,
            saturation=self.saturation,
            value=self.value,
            alpha=self.alpha,
        )


class HWBColor(Color):
    """ A color expressed using its hue, whiteness and blackness components.

        :param hue: Value for :py:attr:`hue`.
        :param whiteness: Value for :py:attr:`whiteness`.
        :param blackness: Value for :py:attr:`blackness`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_hue', '_whiteness', '_blackness')
    _params = ('hue', 'whiteness', 'blackness')

    def __init__(
        self,
        hue: _Angle,
        whiteness: float = 0.0,
        blackness: float = 0.0,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._hue = hue
        self._whiteness = whiteness
        self._blackness = blackness

    def __iter__(self):
        return iter((self.hue, self.whiteness, self.blackness, self.alpha))

    @property
    def hue(self) -> _Angle:
        """ The hue, as an angle. """

        return self._hue

    @property
    def whiteness(self) -> float:
        """ The whiteness, as a value between 0.0 and 1.0. """

        return self._whiteness

    @property
    def blackness(self) -> float:
        """ The blackness, as a value between 0.0 and 1.0. """

        return self._blackness

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        hue, w, bl = self.hue, self.whiteness, self.blackness

        color = HSLColor(hue, 1.0, .5).assrgb()
        r, g, b = color.red, color.green, color.blue

        if w + bl > 1:
            w, bl = map(lambda x: x / (w + bl), (w, bl))

        r, g, b = map(lambda x: x * (1 - w - bl) + w, (r, g, b))

        return SRGBColor(
            red=r,
            green=g,
            blue=b,
            alpha=self.alpha,
        )

    def ashwb(self) -> 'HWBColor':
        """ Get an HWBColor out of the current object. """

        return HWBColor(
            hue=self.hue,
            whiteness=self.whiteness,
            blackness=self.blackness,
            alpha=self.alpha,
        )


class CMYKColor(Color):
    """ A color expressed using its CMYK channels' intensities.

        :param cyan: Value for :py:attr:`cyan`.
        :param magenta: Value for :py:attr:`magenta`.
        :param yellow: Value for :py:attr:`yellow`.
        :param black: Value for :py:attr:`black`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_cyan', '_magenta', '_yellow', '_black')
    _params = ('cyan', 'magenta', 'yellow', 'black')

    def __init__(
        self,
        cyan: float,
        magenta: float,
        yellow: float,
        black: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._cyan = cyan
        self._magenta = magenta
        self._yellow = yellow
        self._black = black

    def __iter__(self):
        return iter((
            self.cyan,
            self.magenta,
            self.yellow,
            self.black,
            self.alpha,
        ))

    @property
    def cyan(self):
        """ Cyan channel intensity between 0.0 and 1.0. """

        return self._cyan

    @property
    def magenta(self):
        """ Magenta channel intensity between 0.0 and 1.0. """

        return self._magenta

    @property
    def yellow(self):
        """ Yellow channel intensity between 0.0 and 1.0. """

        return self._yellow

    @property
    def black(self):
        """ Black channel intensity between 0.0 and 1.0. """

        return self._black

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        c, m, y, k, a = self

        r = 1 - min(1, c * (1 - k) + k)
        g = 1 - min(1, m * (1 - k) + k)
        b = 1 - min(1, y * (1 - k) + k)

        return SRGBColor(
            red=r,
            green=g,
            blue=b,
            alpha=a,
        )

    def ascmyk(self) -> 'CMYKColor':
        """ Get a CMYKColor out of the current object. """

        return CMYKColor(
            cyan=self.cyan,
            magenta=self.magenta,
            yellow=self.yellow,
            black=self.black,
            alpha=self.alpha,
        )


class LABColor(Color):
    """ A color expressed using its CIELAB color space cartesian coordinates.

        :param lightness: Value for :py:attr:`lightness`.
        :param a: Value for :py:attr:`a`.
        :param b: Value for :py:attr:`b`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_lightness', '_a', '_b')
    _params = ('lightness', 'a', 'b')

    def __init__(
        self,
        lightness: float,
        a: float,
        b: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._lightness = lightness
        self._a = a
        self._b = b

    def __iter__(self):
        return iter((self.lightness, self.a, self.b, self.alpha))

    @property
    def lightness(self) -> float:
        """ The CIE lightness.

            Similar to the lightness in the HSL representation.
            Represented as a float between 0.0 and 1.0.
        """

        return self._lightness

    @property
    def a(self) -> float:
        """ The A axis value in the Lab colorspace. """

        return self._a

    @property
    def b(self) -> float:
        """ The B axis value in the Lab colorspace. """

        return self._b

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        raise NotImplementedError  # TODO

    def aslab(self) -> 'LABColor':
        """ Get a LABColor out of the current object. """

        return LABColor(
            lightness=self.lightness,
            a=self.a,
            b=self.b,
            alpha=self.alpha,
        )

    def aslch(self) -> 'LCHColor':
        """ Get a LCHColor out of the current object. """

        l, a, b = self.lightness, self.a, self.b

        return LCHColor(
            lightness=l,
            chroma=_sqrt(a * a + b * b),
            hue=_RadiansAngle(_atan2(b, a)),
            alpha=self.alpha,
        )


class LCHColor(Color):
    """ A color expressed using its CIELAB color space polar coordinates.

        :param lightness: Value for :py:attr:`lightness`.
        :param chroma: Value for :py:attr:`chroma`.
        :param hue: Value for :py:attr:`hue`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_lightness', '_chroma', '_hue', '_alpha')
    _params = ('lightness', 'chroma', 'hue')

    def __init__(
        self,
        lightness: float,
        chroma: float,
        hue: _Angle,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._lightness = lightness
        self._chroma = chroma
        self._hue = hue

    def __iter__(self):
        return iter((self.lightness, self.chroma, self.hue, self.alpha))

    @property
    def lightness(self) -> float:
        """ The CIE lightness.

            Similar to the lightness in the HSL representation.
            Represented as a float between 0.0 and 1.0.
        """

        return self._lightness

    @property
    def chroma(self) -> float:
        """ The chroma.

            Represented as a positive number theoretically  unbounded.
        """

        return self._chroma

    @property
    def hue(self) -> _Angle:
        """ The hue, as an angle. """

        return self._hue

    def aslab(self) -> 'LABColor':
        """ Get a LABColor out of the current object. """

        l, c, h = self.lightness, self.chroma, self.hue.asradians()

        return LABColor(
            lightness=l,
            a=c * _cos(h.radians),
            b=c * _sin(h.radians),
            alpha=self.alpha,
        )

    def aslch(self) -> 'LCHColor':
        """ Get a LCHColor out of the current object. """

        return LCHColor(
            lightness=self.lightness,
            chroma=self.chroma,
            hue=self.hue,
            alpha=self.alpha,
        )


class XYZColor(Color):
    """ A color expressed using its CIEXYZ color space coordinates.

        :param x: Value for :py:attr:`x`.
        :param y: Value for :py:attr:`y`.
        :param z: Value for :py:attr:`z`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_x', '_y', '_z')
    _params = ('x', 'y', 'z')

    def __init__(self, x: float, y: float, z: float, alpha: float = 1.0):
        super().__init__(alpha)

        self._x = x
        self._y = y
        self._z = z

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.alpha))

    @property
    def x(self) -> float:
        """ The CIE X component, between 0.0 and 1.0. """

        return self._x

    @property
    def y(self) -> float:
        """ The CIE Y component, between 0.0 and 1.0. """

        return self._y

    @property
    def z(self) -> float:
        """ The CIE Z component, between 0.0 and 1.0. """

        return self._z

    def asxyz(self) -> 'XYZColor':
        """ Get an XYZColor out of the current object. """

        return self


class YIQColor(Color):
    """ A color expressed using its YIQ components.

        :param y: Value for :py:attr:`y`.
        :param i: Value for :py:attr:`i`.
        :param q: Value for :py:attr:`q`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_y', '_i', '_q')
    _params = ('y', 'i', 'q')

    def __init__(
        self,
        y: float,
        i: float,
        q: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._y = y
        self._i = i
        self._q = q

    def __iter__(self):
        return iter((self.y, self.i, self.q, self.alpha))

    @property
    def y(self) -> float:
        """ The luma. """

        return self._y

    @property
    def i(self) -> float:
        """ The orange-blue range value. """

        return self._i

    @property
    def q(self) -> float:
        """ The purple-green range value. """

        return self._q

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        y, i, q = self.y, self.i, self.q

        return SRGBColor(
            red=max(0.0, min(1.0, (
                y + .9468822170900693 * i + .6235565819861433 * q
            ))),
            green=max(0.0, min(1.0, (
                y - .27478764629897834 * i - .6356910791873801 * q
            ))),
            blue=max(0.0, min(1.0, (
                y - 1.1085450346420322 * i + 1.7090069284064666 * q
            ))),
            alpha=self.alpha,
        )

    def asyiq(self) -> 'YIQColor':
        """ Get an YIQColor out of the current object. """

        return YIQColor(
            y=self.y,
            i=self.i,
            q=self.q,
            alpha=self.alpha,
        )


class YUVColor(Color):
    """ A color expressed using its YUV components.

        :param y: Value for :py:attr:`y`.
        :param u: Value for :py:attr:`u`.
        :param v: Value for :py:attr:`v`.
        :param alpha: Value for :py:attr:`alpha`.
    """

    __slots__ = ('_y', '_u', '_v')
    _params = ('y', 'u', 'v')

    def __init__(
        self,
        y: float,
        u: float,
        v: float,
        alpha: float = 1.0,
    ):
        super().__init__(alpha)

        self._y = y
        self._u = u
        self._v = v

    def __iter__(self):
        return iter((self.y, self.u, self.v, self.alpha))

    @property
    def y(self) -> float:
        """ The luma. """

        return self._y

    @property
    def u(self) -> float:
        """ The U chrominance. """

        return self._u

    @property
    def v(self) -> float:
        """ The V chrominance. """

        return self._v

    def assrgb(self) -> 'SRGBColor':
        """ Get an SRGBColor out of the current object. """

        raise NotImplementedError  # TODO

    def asyuv(self) -> 'YUVColor':
        """ Get an YUVColor out of the current object. """

        return YUVColor(
            y=self.y,
            u=self.u,
            v=self.v,
            alpha=self.alpha,
        )


# End of file.
