#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2019-2022 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
# *****************************************************************************
""" Function and data reference. """

import re as _re

from abc import ABCMeta as _ABCMeta
from collections.abc import Mapping as _Mapping
from enum import auto as _auto, Enum as _Enum
from typing import (
    Any as _Any, Optional as _Optional, Union as _Union,
    Sequence as _Sequence, Tuple as _Tuple, List as _List,
)
from inspect import getfullargspec as _getfullargspec
from itertools import zip_longest as _zip_longest

from .angles import Angle as _Angle
from .colors import (
    Color as _Color, HWBColor as _HWBColor, SRGBColor as _SRGBColor,
)
from .angles import (
    DegreesAngle as _DegreesAngle, GradiansAngle as _GradiansAngle,
    RadiansAngle as _RadiansAngle, TurnsAngle as _TurnsAngle,
)
from .errors import ColorExpressionSyntaxError as _ColorExpressionSyntaxError
from .utils import factor as _factor

__all__ = [
    'ColorDecoder', 'MetaColorDecoder',
    'alias', 'fallback',
]

_NO_DEFAULT_VALUE = type('_NO_DEFAULT_VALUE_TYPE', (), {})()


def _canonicalkey(x):
    """ Get a canonical key for the decoder mapping. """

    return str(x).replace('-', '_').casefold()


def _issubclass(cls, types):
    """ Check if ``cls`` is a subclass of ``types``.

        Until Python 3.10, this function is not aware of the special
        types available in the standard ``typing`` module; this function
        aims at fixing this for Python <= 3.9.
    """

    # Check if is a special case from typing that we know of.

    try:
        origin = types.__origin__
    except AttributeError:
        if types is _Any:
            return True
    else:
        if origin is _Union or origin is _Optional:
            return any(_issubclass(cls, type_) for type_ in types.__args__)

    # If ``types`` is any iterable type (tuple, list, you name it),
    # then we check if the class is a subclass of at least one element
    # in the iterable.

    try:
        types_iter = iter(types)
    except TypeError:
        pass
    else:
        return any(_issubclass(cls, type_) for type_ in types_iter)

    # We default on the base ``issubclass`` from here.

    try:
        return issubclass(cls, types)
    except TypeError:
        return False


def _isinstance(value, types):
    """ Check if ``cls`` is a subclass of ``types``.

        Until Python 3.10, this function is not aware of the special
        types available in the standard ``typing`` module; this function
        aims at fixing this for Python <= 3.9.
    """

    return _issubclass(type(value), types)


def _get_args(func) -> _Sequence[_Tuple[str, _Any, _Any]]:
    """ Get the arguments from a function in order to
        call it using optional or make an alias.

        Each argument is returned as a tuple containing:

            * The name of the argument.
            * The type of the argument.
            * The default value of the argument;
            ``_NO_DEFAULT_VALUE`` if the argument has no default
            value.

        In case an argument is keyword-only with no default
        value, the function will raise an exception.
    """

    # TODO: manage functions with variable positional arguments.

    argspec = _getfullargspec(func)
    try:
        kwarg = next(
            arg
            for arg in argspec.kwonlyargs
            if arg not in (argspec.kwonlydefaults or ())
        )
    except StopIteration:
        pass
    else:
        raise ValueError(
            f'keyword-only argument {kwarg} has no default value',
        )

    annotations = getattr(func, '__annotations__', {})

    argnames = argspec.args
    argtypes = [annotations.get(name) for name in argnames]
    argdefaultvalues = list(argspec.defaults or ())
    argdefaultvalues = (
        [_NO_DEFAULT_VALUE] * (
            len(argspec.args or ()) - len(argdefaultvalues)
        )
        + argdefaultvalues
    )

    return list(zip(argnames, argtypes, argdefaultvalues))


def _make_function(func, name: str, args: _Optional[_Sequence[_Any]]):
    """ Create a function calling another.

        This function will rearrange the given positional
        arguments with the given argument order ``args``.

        It will also set the default value and annotations of
        the previous function, rearranged using the given
        function.
    """

    # Here, we get the variables for the base function call.
    # The resulting variables are the following:
    #
    #  * ``proxy_args``: the proxy arguments as (name, type, defvalue) tuples.
    #  * ``args_index``: a args index -> proxy index correspondance.

    args_spec = _get_args(func)
    args_index: _List[_Optional[int]]

    if not args:
        args_index = list(range(len(args_spec)))
        proxy_args = args_spec
    else:
        args_names = [name for (name, _, _) in args_spec]

        args_index = [None] * len(args_spec)
        proxy_args = []

        for proxy_index_i, arg in enumerate(args):
            try:
                index = args_names.index(arg)
            except ValueError:
                raise ValueError(
                    f'{arg!r} is not an argument of the aliased function'
                )

            args_index[index] = proxy_index_i
            proxy_args.append(args_spec[index])

    # We want to check that no value without a default value was
    # left unspecified.

    for (aname, _, adefvalue), proxy_index in zip(args_spec, args_index):
        if proxy_index is None and adefvalue is _NO_DEFAULT_VALUE:
            raise ValueError(
                f'{aname!r} is left without value in the aliased function',
            )

    # Produce the function code.

    locals_ = {
        '__func': func,
    }

    def _iter_proxy_args(d, args):
        # First, obtain the index of the last optional argument from the
        # end, because even arguments with default values before
        # mandatory arguments cannot have a default value exposed in Python.
        #
        # Then, yield the arguments.

        try:
            mandatory_until = max(
                index for index, (_, _, adefvalue) in enumerate(args)
                if adefvalue is _NO_DEFAULT_VALUE
            )
        except ValueError:
            mandatory_until = -1

        for index, (aname, atype, adefvalue) in enumerate(args):
            atypename = None
            adefvaluename = None

            if atype is not None:
                atypename = f'__type{index}'
                d[atypename] = atype

            if index > mandatory_until and adefvalue is not _NO_DEFAULT_VALUE:
                adefvaluename = f'__value{index}'
                d[adefvaluename] = adefvalue

            yield f'{aname}' + (
                (
                    f': {atypename} = {adefvaluename}',
                    f': {atypename}',
                )[adefvaluename is None],
                (f'={adefvaluename}', '')[adefvaluename is None],
            )[atypename is None]

    def _iter_final_args(d, args_spec, arg_indexes):
        for index, ((aname, _, adefvalue), p_index) in enumerate(
            zip(args_spec, arg_indexes),
        ):
            if p_index is None:
                defvaluename = f'__defvalue{index}'
                d[defvaluename] = adefvalue
                yield defvaluename
            else:
                yield aname

    proxy_args_s = ', '.join(_iter_proxy_args(locals_, proxy_args))
    final_args_s = ', '.join(_iter_final_args(locals_, args_spec, args_index))
    keys = ', '.join(locals_.keys())

    code = (
        f'def __define_alias({keys}):\n'
        f'  def {name}({proxy_args_s}):\n'
        f'    return __func({final_args_s})\n'
        f'  return {name}\n'
        '\n'
        f'__func = __define_alias({keys})\n'
    )

    exec(code, {}, locals_)
    func = locals_['__func']

    return func


def _ncol_func(
    angle: _Angle,
    whiteness: _Union[int, float] = 0,
    blackness: _Union[int, float] = 0,
):
    return _HWBColor(
        hue=angle,
        whiteness=_factor(whiteness),
        blackness=_factor(blackness),
    )


# ---
# Lexer.
# ---


class _ColorExpressionTokenType(_Enum):
    """ Token type. """

    NAME = _auto()
    ANGLE = _auto()
    PERCENTAGE = _auto()
    INTEGER = _auto()
    FLOAT = _auto()
    NCOL = _auto()
    HEX = _auto()
    EMPTY = _auto()
    CALL_START = _auto()
    CALL_END = _auto()

    # Not generated by the lexer.
    CALL = _auto()


class _ColorExpressionToken:
    """ A token as expressed by the color expression lexer. """

    __slots__ = ('_type', '_name', '_value', '_column', '_rawtext')

    TYPE_NAME = _ColorExpressionTokenType.NAME
    TYPE_ANGLE = _ColorExpressionTokenType.ANGLE
    TYPE_PERCENTAGE = _ColorExpressionTokenType.PERCENTAGE
    TYPE_INTEGER = _ColorExpressionTokenType.INTEGER
    TYPE_FLOAT = _ColorExpressionTokenType.FLOAT
    TYPE_NCOL = _ColorExpressionTokenType.NCOL
    TYPE_HEX = _ColorExpressionTokenType.HEX
    TYPE_EMPTY = _ColorExpressionTokenType.EMPTY
    TYPE_CALL_START = _ColorExpressionTokenType.CALL_START
    TYPE_CALL_END = _ColorExpressionTokenType.CALL_END

    # Not generated by the lexer.
    TYPE_CALL = _ColorExpressionTokenType.CALL

    def __init__(
        self,
        type_: _ColorExpressionTokenType,
        name=None,
        value=None,
        column=None,
        rawtext=None,
    ):
        self._type = type_
        self._name = name
        self._value = value
        self._column = column
        self._rawtext = rawtext

    def __repr__(self):
        args = [f'type_=TYPE_{self._type.name}']
        if self._name is not None:
            args.append(f'name={self._name!r}')
        if self._value is not None:
            args.append(f'value={self._value!r}')
        if self._column is not None:
            args.append(f'column={self._column!r}')
        if self._rawtext is not None:
            args.append(f'rawtext={self._rawtext!r}')

        return f'{self.__class__.__name__}({", ".join(args)})'

    @property
    def type_(self):
        """ Token type. """

        return self._type

    @property
    def name(self):
        """ Token name. """

        return self._name

    @property
    def value(self):
        """ Token value. """

        return self._value

    @property
    def column(self):
        """ Column at which the token is located. """

        return self._column

    @property
    def rawtext(self):
        """ Raw text for decoding. """

        return self._rawtext


_colorexpressionpattern = _re.compile(
    r"""
    \s*
    (?P<arg>
        (
            (?P<agl>
                (?P<agl_sign> [+-]?)
                (?P<agl_val> ([0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+)) \s*
                (?P<agl_typ>deg|grad|rad|turns?)
            )
            | (?P<per>
                (?P<per_val>[+-]? [0-9]+(\.[0-9]*)? | [+-]? \.[0-9]+)
                \s* \%
            )
            | (?P<int_val>[+-]? [0-9]+)
            | (?P<flt_val>[+-]? [0-9]+\.[0-9]* | [+-]? \.[0-9]+)
            | (?P<ncol>[RYGCBM] [0-9]{0,2} (\.[0-9]*)?)
            | (
                \# (?P<hex>
                    [0-9a-f]{3} | [0-9a-f]{4}
                    | [0-9a-f]{6} | [0-9a-f]{8}
                )
            )
            | (?P<name> [a-z0-9_-]+)
            |
        ) \s* (?P<sep>,|/|\s|\(|\)|$)
    )
    \s*
    """,
    _re.VERBOSE | _re.I | _re.M,
)


def _get_color_tokens(string: str, extended_hex: bool = False):
    """ Get color tokens.

        :param string: The string to get the color tokens from.
        :param extended_hex: Whether 4 or 8-digit hex colors are
                             allowed (``True``) or not (``False``).
    """

    start: int = 0
    was_call_end: bool = False

    while string:
        match = _colorexpressionpattern.match(string)
        if match is None:
            s = f'{string[:17]}...' if len(string) > 20 else string
            raise _ColorExpressionSyntaxError(
                f'syntax error near {s!r}',
                column=start,
            )

        result = match.groupdict()
        column = start + match.start('arg')

        is_call_end = False

        if result['name']:
            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_NAME,
                value=result['name'],
                column=column,
            )
        elif result['agl'] is not None:
            value = float(result['agl_sign'] + result['agl_val'])
            typ = result['agl_typ']
            if typ == 'deg':
                value = _DegreesAngle(value)
            elif typ == 'rad':
                value = _RadiansAngle(value)
            elif typ == 'grad':
                value = _GradiansAngle(value)
            elif typ in ('turn', 'turns'):
                value = _TurnsAngle(value)
            else:
                raise NotImplementedError

            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_ANGLE,
                value=value,
                column=column,
                rawtext=result['agl'],
            )
        elif result['per'] is not None:
            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_PERCENTAGE,
                value=float(result['per_val']) / 100,
                column=column,
                rawtext=result['per'],
            )
        elif result['int_val'] is not None:
            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_INTEGER,
                value=int(result['int_val']),
                column=column,
                rawtext=result['int_val'],
            )
        elif result['flt_val'] is not None:
            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_FLOAT,
                value=float(result['flt_val']),
                column=column,
                rawtext=result['flt_val'],
            )
        elif result['ncol'] is not None:
            letter = result['ncol'][0]
            number = float(result['ncol'][1:])

            if number < 0 or number >= 100:
                yield _ColorExpressionToken(
                    _ColorExpressionToken.TYPE_NAME,
                    value=result['ncol'],
                    column=column,
                )
            else:
                yield _ColorExpressionToken(
                    _ColorExpressionToken.TYPE_NCOL,
                    value=_DegreesAngle(
                        'RYGCBM'.find(letter) * 60 + number / 100 * 60
                    ),
                    column=column,
                    rawtext=result['ncol'],
                )
        elif result['hex'] is not None:
            value_s = result['hex']
            if len(value_s) in (4, 8) and not extended_hex:
                raise _ColorExpressionSyntaxError(
                    f'extended hex values are forbidden: {"#" + value_s!r}',
                    column=start,
                )

            if len(value_s) <= 4:
                value_s = ''.join(map(lambda x: x + x, value_s))

            r = int(value_s[0:2], 16)
            g = int(value_s[2:4], 16)
            b = int(value_s[4:6], 16)
            a = int(value_s[6:8], 16) / 255.0 if len(value_s) == 8 else 1.0

            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_HEX,
                value=_SRGBColor.frombytes(r, g, b, a),
                column=column,
                rawtext='#' + result['hex'],
            )
        else:
            # ``was_call_end`` hack: take ``func(a, b) / c`` for example.
            # By default, it is tokenized as the following:
            #
            #  * name 'func'
            #  * call start
            #  * name 'a'
            #  * name 'b'
            #  * call end
            #  * empty arg [1]
            #  * name 'c'
            #
            # The empty arg at [1] is tokenized since an argument could
            # directly be after the right parenthesis. However, we do not
            # want this to be considered an empty arg, so we ignore empty
            # args right after call ends.
            #
            # Note that ``func(a, b) / / c`` will still contain an empty
            # argument before name 'c'.

            if not was_call_end:
                yield _ColorExpressionToken(
                    _ColorExpressionToken.TYPE_EMPTY,
                    column=column,
                    rawtext='',
                )

        sep = result['sep']
        column = start + match.start('sep')

        if sep == '(':
            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_CALL_START,
                column=column,
                rawtext=sep,
            )
        elif sep == ')':
            is_call_end = True
            yield _ColorExpressionToken(
                _ColorExpressionToken.TYPE_CALL_END,
                column=column,
                rawtext=sep,
            )

        start += match.end()
        string = string[match.end():]
        was_call_end = is_call_end


# ---
# Base decoder classes.
# ---

def fallback(value: _Union[_Color, _Angle, int, float]):
    """ Decorator for setting a fallback value on a function.

        When a function is used as a symbol instead of a function,
        by default, it yields that it is callable and should be
        accompanied with arguments.

        Using this decorator on a function makes it to be evaluated
        as a color in this case.
    """

    if not isinstance(value, (_Color, _Angle, int, float)):
        raise ValueError(
            'fallback value should be a color, an angle or a number, '
            f'is {value!r}',
        )

    def decorator(func):
        func.__fallback_value__ = value
        return func

    return decorator


class alias:
    """ Define an alias for a function. """

    __slots__ = ('_name', '_args')

    def __init__(self, name: str, args: _Sequence[str] = ()):
        self._name = name
        self._args = tuple(args)

        if len(self._args) != len(set(self._args)):
            raise ValueError('arguments should be unique')
        if any(not x or not isinstance(x, str) for x in self._args):
            raise ValueError('all arguments should be non-empty strings')

    @property
    def name(self):
        return self._name

    @property
    def args(self) -> _Sequence[str]:
        return self._args


class ColorDecoder(_Mapping):
    """ Base color decoder.

        This color decoder behaves as a mapping returning syntax elements,
        with the additional properties controlling its behaviour.

        The properties defined at class definition time are the following:

        ``__mapping__``

            Defines the base mapping that is copied at the
            instanciation of each class.

        ``__ncol_support__``

            Defines whether natural colors (NCol) are
            supported while decoding or not.

        ``__extended_hex_support__``

            Defines whether 4 or 8-digit
            hexadecimal colors (starting with a '#') are allowed or not.

        ``__defaults_to_netscape_color``

            Defines whether color decoding
            defaults to Netscape color parsing or not.

        These properties cannot be changed at runtime, although they might
        be in a future version of thcolor.
    """

    __slots__ = ('_mapping',)
    __mapping__: _Mapping = {}
    __ncol_support__: bool = False
    __extended_hex_support__: bool = False
    __defaults_to_netscape_color__: bool = True

    def __init__(self):
        cls = self.__class__

        mapping = {}
        for key, value in cls.__mapping__.items():
            mapping[_canonicalkey(key)] = value

        self._mapping = mapping
        self._ncol_support = cls.__ncol_support__
        self._extended_hex_support = cls.__extended_hex_support__
        self._defaults_to_netscape_color = cls.__defaults_to_netscape_color__

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __getitem__(self, key):
        return self._mapping[_canonicalkey(key)]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def decode(
        self,
        expr: str,
        prefer_colors: bool = False,
        prefer_angles: bool = False,
    ) -> _Sequence[_Optional[_Union[_Color, _Angle, int, float]]]:
        """ Decode a color expression.

            When top-level result(s) are not colors and colors are
            actually expected if possible to obtain, the caller should
            set ``prefer_colors`` to ``True`` in order for top-level
            conversions to take place.

            Otherwise, when top-level result(s) are not angles and angles
            are actually expected if possible to obtain, the caller should
            set ``prefer_angles`` to ``True`` in order for top-level
            conversions to take place.
        """

        global _color_pattern

        ncol_support = bool(self._ncol_support)
        extended_hex_support = bool(self._extended_hex_support)
        defaults_to_netscape = bool(self._defaults_to_netscape_color)

        # Parsing stage; the results will be in ``current``.
        #
        # * ``stack``: the stack of current values.
        # * ``func_stack``: the function name or special type, as tokens.
        #   Accepted token types here are ``NAME`` and ``NCOL``.
        # * ``implicit_stack``: when the current function is an implicit
        #   one, this stack contains the arguments left to read in this
        #   implicit function.
        # * ``current``: the current list of elements, which is put on
        #   top of the stack when a call is started and is popped out of
        #   the top of the stack when a call is ended.

        stack: _List[_List[_ColorExpressionToken]] = []
        func_stack: _List[_ColorExpressionToken] = []
        implicit_stack: _List[int] = []
        current: _List[_ColorExpressionToken] = []

        def _get_parent_func():
            """ Get the parent function name for exceptions. """

            if not func_stack:
                return None
            if func_stack[0].type_ == _ColorExpressionToken.TYPE_NCOL:
                return '<implicit ncol function>'
            return func_stack[0].value

        token_iter = _get_color_tokens(
            expr,
            extended_hex=extended_hex_support,
        )
        for token in token_iter:
            if (
                token.type_ == _ColorExpressionToken.TYPE_NCOL
                and ncol_support
            ):
                func_stack.insert(0, token)
                stack.insert(0, current)
                implicit_stack.insert(0, 3)
                current = []
            elif token.type_ == _ColorExpressionToken.TYPE_NCOL:
                current.append(_ColorExpressionToken(
                    _ColorExpressionToken.TYPE_NAME,
                    value=token.rawtext,
                    rawtext=token.rawtext,
                    column=token.column,
                ))
            elif token.type_ in (
                _ColorExpressionToken.TYPE_NAME,
                _ColorExpressionToken.TYPE_ANGLE,
                _ColorExpressionToken.TYPE_PERCENTAGE,
                _ColorExpressionToken.TYPE_INTEGER,
                _ColorExpressionToken.TYPE_FLOAT,
                _ColorExpressionToken.TYPE_HEX,
                _ColorExpressionToken.TYPE_EMPTY,
            ):
                # Current token is a value, we simply add it.

                current.append(token)
            elif token.type_ == _ColorExpressionToken.TYPE_CALL_START:
                if func_stack and (
                    func_stack[0].type_ == _ColorExpressionToken.TYPE_NCOL
                ):
                    implicit_stack[0] += 1

                name_token = current.pop(-1)
                if name_token.type_ != _ColorExpressionToken.TYPE_NAME:
                    raise _ColorExpressionSyntaxError(
                        'expected the name of the function to call, '
                        f'got a {name_token.type_.name}',
                        column=name_token.column,
                        func=_get_parent_func(),
                    )

                func_stack.insert(0, name_token)
                stack.insert(0, current)
                current = []
            elif token.type_ == _ColorExpressionToken.TYPE_CALL_END:
                # First, pop out all of the implicit functions.

                while func_stack:
                    try:
                        name_token = func_stack.pop(0)
                    except IndexError:
                        raise _ColorExpressionSyntaxError(
                            'extraneous closing parenthesis',
                            column=token.column,
                            func=_get_parent_func(),
                        ) from None

                    if name_token.type_ == _ColorExpressionToken.TYPE_NAME:
                        break

                    # We just pop the function out of the stack with the
                    # arguments we have.

                    implicit_stack.pop(0)
                    old_current = stack.pop(0)
                    old_current.append(_ColorExpressionToken(
                        type_=_ColorExpressionToken.TYPE_CALL,
                        column=name_token.column,
                        name=_ncol_func,
                        value=(name_token, *current),
                    ))
                    current = old_current

                # We have a function name and it is not implicit.

                old_current = stack.pop(0)
                old_current.append(_ColorExpressionToken(
                    _ColorExpressionTokenType.CALL,
                    name=name_token.value,
                    value=current,
                    column=name_token.column,
                ))
                current = old_current
            else:
                raise NotImplementedError(
                    f'unknown token type: {token.type_!r}',
                )

            if func_stack and (
                func_stack[0].type_ == _ColorExpressionToken.TYPE_NCOL
            ):
                implicit_stack[0] -= 1
                if implicit_stack[0] <= 0:
                    ncol = func_stack.pop(0)
                    implicit_stack.pop(0)

                    # We have the required number of tokens for this
                    # to work.

                    old_current = stack.pop(0)
                    old_current.append(_ColorExpressionToken(
                        type_=_ColorExpressionToken.TYPE_CALL,
                        column=ncol.column,
                        name=_ncol_func,
                        value=(ncol, *current),
                    ))
                    current = old_current

        # We want to pop out all implicit functions we have.
        # If we still have an explicit function in the function stack,
        # that means a parenthesis was omitted.

        while func_stack:
            try:
                name_token = func_stack.pop(0)
            except IndexError:
                break

            if name_token.type_ == _ColorExpressionToken.TYPE_NAME:
                raise _ColorExpressionSyntaxError(
                    'missing closing parenthesis',
                    column=len(expr),
                    func=_get_parent_func(),
                )

            # We just pop the function out of the stack with the
            # arguments we have.

            implicit_stack.pop(0)
            old_current = stack.pop(0)
            old_current.append(_ColorExpressionToken(
                type_=_ColorExpressionToken.TYPE_CALL,
                column=name_token.column,
                name=_ncol_func,
                value=(name_token, *current),
            ))
            current = old_current

        # Evaluating stage.

        def evaluate(element, parent_func=None):
            """ Evaluate the element in the current context.

                Always returns a tuple where:

                 * The first element is the real answer.
                 * The second element is the string which can be used
                   in the case of a color fallback (when Netscape color
                   defaulting is on).
            """

            if element.type_ == _ColorExpressionTokenType.NAME:
                try:
                    data = self[element.value]
                except KeyError:
                    if defaults_to_netscape:
                        return (
                            _SRGBColor.fromnetscapecolorname(element.value),
                            element.value,
                        )

                    raise _ColorExpressionSyntaxError(
                        f'unknown value {element.value!r}',
                        column=element.column,
                        func=parent_func,
                    )
                else:
                    if not isinstance(data, (_Color, _Angle, int, float)):
                        try:
                            fallback_value = data.__fallback_value__
                        except AttributeError:
                            raise _ColorExpressionSyntaxError(
                                f'{element.value!r} is not a value and '
                                f'has no fallback value (is {data!r})',
                                column=element.column,
                                func=parent_func,
                            )

                        if not isinstance(fallback_value, (
                            _Color, _Angle, int, float,
                        )):
                            raise _ColorExpressionSyntaxError(
                                f'{element.value!r} fallback value '
                                f'{fallback_value!r} is not a color, '
                                'an angle or a number.',
                                column=element.column,
                                func=parent_func,
                            )

                        data = fallback_value

                    return (data, element.value)
            elif element.type_ != _ColorExpressionTokenType.CALL:
                return (element.value, element.rawtext)

            func_name = element.name
            if callable(func_name):
                func = func_name
                func_name = '<implicit ncol function>'
            else:
                try:
                    func = self[func_name]
                except KeyError:
                    raise _ColorExpressionSyntaxError(
                        f'function {func_name!r} not found',
                        column=element.column,
                        func=parent_func,
                    )

            # Check the function.

            try:
                args_spec = _get_args(func)
            except ValueError as exc:
                raise _ColorExpressionSyntaxError(
                    f'function {func_name!r} is unsuitable for '
                    f'calling: {str(exc)}',
                    column=element,
                    func=parent_func,
                )

            # Check the argument count.
            #
            # We remove empty arguments at the end of calls so that
            # even calls such as ``func(a, b, , , , , ,)`` will only
            # have arguments 'a' and 'b'.

            unevaluated_args = element.value
            while (
                unevaluated_args and unevaluated_args[-1].type_
                == _ColorExpressionToken.TYPE_EMPTY
            ):
                unevaluated_args.pop(-1)

            if len(unevaluated_args) > len(args_spec):
                raise _ColorExpressionSyntaxError(
                    f'too many arguments for {func_name!r}: '
                    f'expected {len(args_spec)}, got {len(unevaluated_args)}',
                    column=element.column,
                    func=parent_func,
                )

            # Now we should evaluate subtokens and check the types of
            # the function.

            new_args = []

            for token, (argname, argtype, argdefvalue) in _zip_longest(
                unevaluated_args, args_spec, fillvalue=None,
            ):
                arg, fallback_string, column = None, None, element.column
                if token is not None:
                    column = token.column
                    arg, *_, fallback_string = evaluate(token)

                arg = arg if arg is not None else argdefvalue
                if arg is _NO_DEFAULT_VALUE:
                    raise _ColorExpressionSyntaxError(
                        f'expected a value for {argname!r}',
                        column=column,
                        func=func_name,
                    )

                if argtype is None or _isinstance(arg, argtype):
                    pass
                elif (
                    _issubclass(_Color, argtype) and defaults_to_netscape
                    and fallback_string is not None
                ):
                    arg = _SRGBColor.fromnetscapecolorname(fallback_string)
                elif (
                    _issubclass(_Angle, argtype)
                    and isinstance(arg, (int, float))
                ):
                    arg = _DegreesAngle(arg)
                elif (
                    _issubclass(float, argtype)
                    and isinstance(arg, int)
                ):
                    arg = float(arg)
                elif (
                    _issubclass(int, argtype)
                    and isinstance(arg, float)
                    and arg == int(arg)
                ):
                    arg = int(arg)
                else:
                    raise _ColorExpressionSyntaxError(
                        f'{arg!r} did not match expected type {argtype!r}'
                        f' for argument {argname!r}',
                        column=column,
                        func=func_name,
                    )

                new_args.append(arg)

            # Get the result.

            result = func(*new_args)
            if result is None:
                raise _ColorExpressionSyntaxError(
                    f'function {func_name!r} returned an empty '
                    'result for the following arguments: '
                    f'{", ".join(map(repr, new_args))}.',
                    column=token.column,
                    func=parent_func,
                )

            return result, None

        return tuple(
            _SRGBColor.fromnetscapecolorname(fallback_string)
            if (
                not isinstance(result, _Color)
                and prefer_colors
                and defaults_to_netscape
                and fallback_string is not None
            )
            else _DegreesAngle(result)
            if (
                isinstance(result, (int, float))
                and prefer_angles
            )
            else result
            for result, *_, fallback_string in map(evaluate, current)
        )


# ---
# Meta base type.
# ---


class _MetaColorDecoderType(_ABCMeta):
    """ The decoder type. """

    def __new__(mcls, clsname, superclasses, attributedict):
        elements = {}
        options = {
            '__ncol_support__': False,
            '__extended_hex_support__': False,
            '__defaults_to_netscape_color__': False,
        }

        # Explore the parents.

        for supercls in reversed(superclasses):
            if not issubclass(supercls, ColorDecoder):
                continue

            for option in options:
                if getattr(supercls, option, False):
                    options[option] = True

            elements.update(supercls.__mapping__)

        for option, value in options.items():
            options[option] = attributedict.get(option, value)

        # Instanciate the class.

        clsattrs = {
            '__doc__': attributedict.get('__doc__', None),
            '__mapping__': elements,
        }
        clsattrs.update(options)

        cls = super().__new__(mcls, clsname, superclasses, clsattrs)
        del clsattrs

        # Get the elements and aliases from the current attribute dictionary.

        aliases = {}
        childelements = {}
        for key, value in attributedict.items():
            if key.startswith('_') or key.endswith('_'):
                continue

            key = _canonicalkey(key)

            if isinstance(value, alias):
                aliases[key] = value
                continue
            elif callable(value):
                pass
            elif isinstance(value, (int, float, _Color, _Angle)):
                value = value
            else:
                raise TypeError(
                    f'{clsname} property {key!r} is neither an alias, '
                    'a function, a number, a color or an angle',
                )

            childelements[key] = value

        # Resolve the aliases.
        #
        # Because of dependencies, we do the basic solution for that:
        # We try to resolve aliases as we can, ignoring the ones for which
        # the aliases are still awaiting. If we could not resolve any
        # of the aliases in one round and there still are some left,
        # there must be a cyclic dependency somewhere.
        #
        # This is not optimized. However, given the cases we have,
        # it'll be enough.

        aliaselements = {}
        while aliases:
            resolved = len(aliases)
            nextaliases = {}

            for key, alias_value in aliases.items():
                funcname = _canonicalkey(alias_value.name)

                # Check if the current alias still depends on an alias
                # that hasn't been resolved yet; in that case, ignore
                # it for now.

                if funcname in aliases:
                    resolved -= 1
                    nextaliases[key] = alias_value
                    continue

                # Check the function name and arguments.

                try:
                    func = childelements[funcname]
                except KeyError:
                    try:
                        func = elements[funcname]
                    except KeyError:
                        raise ValueError(
                            f'{clsname} property {key!r} references '
                            f'undefined function {funcname!r}',
                        ) from None

                if not callable(func):
                    raise ValueError(
                        f'{clsname} property {key!r} '
                        f'references non-function {funcname!r}',
                    )

                aliaselements[_canonicalkey(key)] = _make_function(
                    func, name=key.replace('-', '_'), args=alias_value.args,
                )

            aliases = nextaliases
            if aliases and not resolved:
                raise ValueError(
                    f'could not resolve left aliases in class {clsname}, '
                    'there might be a cyclic dependency between these '
                    'aliases: ' + ', '.join(aliases.keys()) + '.',
                )

        # Add all of the elements in order of importance.

        elements.update(aliaselements)
        elements.update(childelements)

        # Check the types of the annotations, just in case.

        for key, element in elements.items():
            try:
                args_spec = _get_args(element)
            except TypeError:
                continue

            for argname, argtype, argdefvalue in args_spec:
                if argtype is None:
                    continue

                if all(
                    not _issubclass(type_, argtype)
                    for type_ in (int, float, _Color, _Angle, type(None))
                ):
                    raise TypeError(
                        f'function {key!r}, argument {argname!r}: '
                        'none of the types handled by the decoder are '
                        f'valid subclasses of type hint {argtype}',
                    )

                if argdefvalue is _NO_DEFAULT_VALUE:
                    continue

                if (
                    not _isinstance(argdefvalue, argtype)
                    and not (
                        isinstance(argdefvalue, int)
                        and _issubclass(float, argtype)
                    )
                    and not (
                        isinstance(argdefvalue, float)
                        and int(argdefvalue) == argdefvalue
                        and _issubclass(int, argtype)
                    )
                    and not (
                        isinstance(argdefvalue, (int, float))
                        and _issubclass(_Angle, argtype)
                    )
                ):
                    raise TypeError(
                        f'function {key!r}, argument {argname!r}: '
                        f'default value {argdefvalue!r} is not a valid '
                        f'instance of type hint {argtype!r}',
                    )

        return cls


class MetaColorDecoder(ColorDecoder, metaclass=_MetaColorDecoderType):
    """ Base meta color decoder, which gets the function and things. """

    pass


# End of file.
