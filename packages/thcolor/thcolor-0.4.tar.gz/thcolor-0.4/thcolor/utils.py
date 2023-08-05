#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2022 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
# *****************************************************************************
""" Utilities for the thcolor module. """

from typing import Optional as _Optional

__all__ = ['factor', 'round_half_up']


def factor(x, max_: int = 100, clip: bool = False):
    """ Return a factor based on if something is a float or an int. """

    if isinstance(x, float):
        pass
    elif x in (0, 1) and max_ == 100:
        x = float(x)
    else:
        x /= max_

    if clip:
        x = max(0, min(1, x))

    return x


def round_half_up(number: float, ndigits: _Optional[int] = None) -> float:
    """ Round a number to the nearest integer.

        This function exists because Python's built-in ``round`` function
        uses half-to-even rounding, also called "Banker's rounding".
        This means that 1.5 is rounded to 2 and 2.5 is also rounded to 2.

        What we want is a half-to-up rounding, so we have this function.
    """

    if ndigits is None:
        ndigits = 0

    base = 10 ** -ndigits

    return (number // base) * base + (
        base if (number % base) >= (base / 2) else 0
    )


# End of file.
