Color representations
=====================

thcolor allows you to represent colors in different colorspaces and using
different kind of coordinates. This page regroups the information about these
representations.

Note that all color representations have an ``alpha`` component.

sRGB colors
-----------

sRGB colors are colors represented using the red, green and blue channel
intensities in the `standard RGB color space`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.SRGBColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.assrgb`
("as sRGB") method.

CMYK colors
-----------

CMYK colors are colors represented using the cyan, magenta, yellow and
black values in the `CMYK color model`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.CMYKColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.ascmyk` method.

HSL colors
----------

HSL colors are colors represented using the hue, saturation and lightness
as polar coordinates in the sRGB color space. See `HSL and HSV`_ for more
information.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.HSLColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.ashsl` method.

HSV colors
----------

HSV colors are colors represented using the hue, saturation and value
as polar coordinates in the sRGB color space. See `HSL and HSV`_ for
more information.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.HSVColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.ashsv` method.

.. _hwb-colors:

HWB colors
----------

HWB colors are colors represented using the hue, whiteness and blackness
in the `HWB color model`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.HWBColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.ashwb` method.

LAB colors
----------

LAB colors are colors represented using the lightness and A and B coordinates
in the `CIELAB color space`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.LABColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.aslab` method.

LCH colors
----------

LCH colors are colors represented using the lightness, chroma and hue
in the `CIELAB color space`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.LCHColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.aslch` method.

XYZ colors
----------

XYZ colors are colors represented using its x, y and z coordinates
in the `CIE 1931 XYZ color space`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.XYZColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.asxyz`
method.

YIQ colors
----------

YIQ colors are colors represented using its coordinates in the
`YIQ color space`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.YIQColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.asyiq` method.

YUV colors
----------

YUV colors are colors represented using its coordinates in the
`YUV color space`_.

In thcolor, such a color is represented by the
:py:class:`thcolor.colors.YUVColor` class, and other representations can be
converted to this one using the :py:meth:`thcolor.colors.Color.asyuv`
method.

.. _natural-colors:

Natural colors
--------------

Natural colors (NCol) are an initiative from W3Schools to make a color
that is easily identifiable from reading its definition.

In thcolor, no dedicated class exists for this representation since it is
a light derivative from :ref:`HWB colors <hwb-colors>` with the angle
expressed using a given format. It is, however, optionally supported
in expressions behind the ``__ncol_support__`` option.

.. _standard RGB color space: https://en.wikipedia.org/wiki/SRGB
.. _CMYK color model: https://en.wikipedia.org/wiki/CMYK_color_model
.. _HSL and HSV: https://en.wikipedia.org/wiki/HSL_and_HSV
.. _HWB color model: https://en.wikipedia.org/wiki/HWB_color_model
.. _CIELAB color space: https://en.wikipedia.org/wiki/CIELAB_color_space
.. _CIE 1931 XYZ color space: https://en.wikipedia.org/wiki/CIE_1931_color_space
.. _YIQ color space: https://en.wikipedia.org/wiki/YIQ
.. _YUV color space: https://en.wikipedia.org/wiki/YUV
.. _`natural colors`: https://www.w3schools.com/colors/colors_ncol.asp
