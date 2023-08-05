#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2019-2022 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
# *****************************************************************************
""" Angle representation and conversions. """

from math import pi as _pi
from typing import Any as _Any, Optional as _Optional

__all__ = [
    'Angle', 'DegreesAngle', 'GradiansAngle', 'RadiansAngle', 'TurnsAngle',
]


class Angle:
    """ Abstract class representing an angle within thcolor.

        Used for some color representations (most notably hue).
    """

    __slots__ = ()

    _value: float
    _bottom: float = 0
    _top: float = 1

    def __init__(self):
        pass

    def __repr__(self):
        params = (
            (key, getattr(self, key)) for key in dir(self)
            if not key.startswith('_') and not callable(getattr(self, key))
        )

        return (
            f'{self.__class__.__name__}('
            f"{', '.join(f'{key}={val!r}' for key, val in params)})"
        )

    def __eq__(self, other):
        if not isinstance(other, Angle):
            return False

        return (
            round(self.asturns().turns, 6) == round(other.asturns().turns, 6)
        )

    def asdegrees(self) -> 'DegreesAngle':
        """ Get the current angle as a degrees angle. """

        try:
            value = self._value
            ob = self._bottom
            ot = self._top
        except AttributeError:
            raise NotImplementedError from None

        nb = DegreesAngle._bottom
        nt = DegreesAngle._top

        return DegreesAngle((value - ob) / (ot - ob) * (nt - nb) + nb)

    def asgradians(self) -> 'GradiansAngle':
        """ Get the current angle as a gradians angle. """

        try:
            value = self._value
            ob = self._bottom
            ot = self._top
        except AttributeError:
            raise NotImplementedError from None

        nb = GradiansAngle._bottom
        nt = GradiansAngle._top

        return GradiansAngle((value - ob) / (ot - ob) * (nt - nb) + nb)

    def asradians(self) -> 'RadiansAngle':
        """ Get the current angle as a radians angle. """

        try:
            value = self._value
            ob = self._bottom
            ot = self._top
        except AttributeError:
            raise NotImplementedError from None

        nb = RadiansAngle._bottom
        nt = RadiansAngle._top

        return RadiansAngle((value - ob) / (ot - ob) * (nt - nb) + nb)

    def asturns(self) -> 'TurnsAngle':
        """ Get the current angle as a turns angle. """

        try:
            value = self._value
            ob = self._bottom
            ot = self._top
        except AttributeError:
            raise NotImplementedError from None

        nb = TurnsAngle._bottom
        nt = TurnsAngle._top

        return TurnsAngle((value - ob) / (ot - ob) * (nt - nb) + nb)

    def asprincipal(self):
        """ Get the principal angle. """

        cls = self.__class__
        value = self._value
        bottom, top = cls._bottom, cls._top

        return cls((value - bottom) % (top - bottom) + bottom)

    @classmethod
    def fromtext(
        cls,
        expr: str,
        decoder: _Optional[_Any] = None,
    ) -> 'Angle':
        """ Create a color from a string.

            :param expr: The expression to decode.
        """

        if decoder is None:
            from .builtin import DefaultColorDecoder

            decoder = DefaultColorDecoder()

        results = decoder.decode(expr, prefer_angles=True)

        if len(results) != 1 or not isinstance(results[0], cls):
            raise ValueError(
                f'result of expression was not an instance of {cls.__name__}: '
                f'single color: {results!r}',
            )

        return results[0]


class DegreesAngle(Angle):
    """ An angle expressed in degrees.

        A 270° angle can be created the following way:

        .. code-block:: python

            angle = DegreesAngle(270)

        :param degrees: Degrees; canonical values are between 0 and 360
                        excluded.
    """

    __slots__ = ('_value')

    _bottom = 0
    _top = 360.0

    def __init__(self, degrees: float):
        self._value = float(degrees)  # % 360.0

    def __str__(self):
        x = self._value
        return f'{int(x) if x == int(x) else x}deg'

    @property
    def degrees(self) -> float:
        """ Degrees. """

        return self._value


class GradiansAngle(Angle):
    """ An angle expressed in gradians.

        A 565.5 gradians angle can be created the following way:

        .. code-block:: python

            angle = GradiansAngle(565.5)

        :param gradians: Gradians; canonical values are between
                          0 and 400.0 excluded.
    """

    __slots__ = ('_value')

    _bottom = 0
    _top = 400.0

    def __init__(self, gradians: float):
        self._value = float(gradians)  # % 400.0

    def __str__(self):
        x = self._value
        return f'{int(x) if x == int(x) else x}grad'

    @property
    def gradians(self) -> float:
        """ Gradians. """

        return self._value


class RadiansAngle(Angle):
    """ An angle expressed in radians.

        A π radians angle can be created the following way:

        .. code-block:: python

            from math import pi
            angle = RadiansAngle(pi)

        :param radians: Radians; canonical are between 0 and 2π
                         excluded.
    """

    __slots__ = ('_value')

    _bottom = 0
    _top = 2 * _pi

    def __init__(self, radians: float):
        self._value = float(radians)  # % (2 * _pi)

    def __str__(self):
        x = self._value
        return f'{int(x) if x == int(x) else x}rad'

    def __repr__(self):
        r = self.radians / _pi
        ir = int(r)
        if r == ir:
            r = ir

        return f"{self.__class__.__name__}(radians = {f'{r}π' if r else '0'})"

    @property
    def radians(self) -> float:
        """ Radians. """

        return self._value


class TurnsAngle(Angle):
    """ An angle expressed in turns.

        A 3.5 turns angle can be created the following way:

        .. code-block:: python

            angle = TurnsAngle(3.5)

        :param turns: Turns; canonical values are between 0 and 1
                      excluded.
    """

    __slots__ = ('_value')

    _bottom = 0
    _top = 1

    def __init__(self, turns: float):
        self._value = float(turns)  # % 1.0

    def __str__(self):
        x = self._value
        return f'{int(x) if x == int(x) else x}turn'

    @property
    def turns(self) -> float:
        """ Turns. """

        return self._value

# End of file.
