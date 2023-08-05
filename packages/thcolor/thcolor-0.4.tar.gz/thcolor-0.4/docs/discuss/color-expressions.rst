.. _expr:

Color expressions
=================

One of the aims of thcolor was to decode text-based expressions
representing colors with possibilities challenging and even outdo
CSS color expression possibilities. In thcolor, these expressions are
evaluated using :py:meth:`thcolor.decoders.ColorDecoder.decode`,
:py:meth:`thcolor.colors.Color.fromtext` or
:py:meth:`thcolor.angles.Angle.fromtext`.

Concepts
--------

The goal of these expressions was to embrace and extend CSS syntax, so they
are basically either basic expressions or function calls, with the following
argument types:

 * Numbers.
 * Percentages.
 * Angles.
 * Colors.

These elements are separated by separators (either commas, slashes, or simple
spaces) and can be passed to functions, and the calls themselves can be passed
to other functions. A function call is made in the following fashion:

::

	<function name>([<number | percentage | angle | color> [<separator> …]])

If at least one separator (even simple spaces) are required between arguments,
extraneous separators between and after the arguments are ignored. Other than
if spaces are used as separators, spaces around the parenthesis or the
separators (and "between" the separators as spaces are recognized as
separators) are ignored.

Here are some example calls:

::

	rgb(1, 2, 3)
	rgb  ( 1 22 //// 242 , 50.0% ,/,)
	hsl (0 1 50 % / 22)
	gray ( red( #123456 )/0.2/)

.. _explain-decoders:

Decoders
--------

Decoders are the tools within thcolor that handle the actual evaluation of
expressions. They have two important components aside from the decoding
function:

* Options defining the behaviour of base parsing and evaluating.
* A reference of functions, colors and other data indexed by name.

The options currently available are the following:

* Whether natural colors are enabled or not; see :ref:`natural-colors`.
* Whether extended hexadecimal colors, i.e. 4 or 8 digit hexadecimal digits
  preceded with a '#' sign, which includes transparency, are enabled or not.
* Whether names that are not found should be resolved using Netscape-like
  color parsing or not, what is also known as "quirks mode".

The reference contains three kinds of elements, all indexed by name:

* Constants, always to be used as values, e.g. the ``navy`` color.
* Functions, always to be used by calling them, e.g. the ``rgb`` function.
* Functions with fallbacks, which have a behaviour when called and a fallback
  value when used as a value, e.g. the ``red`` function in the extended
  color decoder which extracts the red channel value as a function and acts
  as the color ``red`` if used as a value.

Decoders can be defined using two base classes which act in a very different
way:

* **The manual way.**
  You can define a decoder manually by making it inherit from
  :py:class:`thcolor.decoders.ColorDecoder` and overriding
  ``__mapping__`` to define the reference, and other double-underscore
  properties for options.
* **The user-friendly way.**
  You can define a decoder in an easier way by making it inherit from
  :py:class:`thcolor.decoders.MetaColorDecoder` and defining options,
  functions and data by defining them directly in the class body;
  see :ref:`defining-decoders` for more information.
