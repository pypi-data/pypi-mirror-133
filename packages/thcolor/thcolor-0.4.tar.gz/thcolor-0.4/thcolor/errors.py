#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2019-2022 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
# *****************************************************************************
""" Exception definitions. """

__all__ = [
    'ColorExpressionSyntaxError',
]


class ColorExpressionSyntaxError(Exception):
    """ An error has occurred while decoding a color expression.

        Such an error can happen during parsing or evaluating.
    """

    def __init__(self, text, column=None, func=None):
        self._column = column if column is not None and column >= 0 else None
        self._func = str(func) if func else None
        self._text = str(text) if text else ''

    def __str__(self):
        msg = ''

        if self._column is not None:
            msg += f'at column {self._column}'
            if self._func is not None:
                msg += ', '
        if self._func is not None:
            msg += f'for function {self._func!r}'
        if msg:
            msg += ': '

        return msg + self._text

    @property
    def text(self):
        """ Exception message, usually linked to the context. """

        return self._text

    @property
    def column(self):
        """ Column of the expression at which the exception has occurred.

            ``None`` if the error has occurred on an unknown column or on
            the whole exception.
        """

        return self._column

    @property
    def func(self):
        """ Name of the function we were calling when the error occurred.

            Either on arguments decoding or erroneous argument type or value.
            Is ``None`` if the context is unknown or the error hasn't
            occurred while calling a function or decoding its
            arguments.
        """

        return self._func


# End of file.
