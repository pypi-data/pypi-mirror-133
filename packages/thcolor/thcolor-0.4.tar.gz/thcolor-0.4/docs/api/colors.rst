Colors API
==========

.. py:module:: thcolor.colors

The base class for colors is the following:

.. autoclass:: Color
    :members: alpha, assrgb, ashsl, ashsv, ashwb, ascmyk, aslab, aslch, asxyz,
              asyiq, asyuv, fromtext, replace, darker, lighter, desaturate,
              saturate, css

Subclasses are the following:

.. autoclass:: CMYKColor
    :members: cyan, magenta, yellow, black, alpha

.. autoclass:: HSLColor
    :members: hue, saturation, lightness, alpha

.. autoclass:: HSVColor
    :members: hue, saturation, value, alpha

.. autoclass:: HWBColor
    :members: hue, whiteness, blackness, alpha

.. autoclass:: LABColor
    :members: lightness, a, b, alpha

.. autoclass:: LCHColor
    :members: lightness, chroma, hue, alpha

.. autoclass:: SRGBColor
    :members: red, green, blue, alpha, frombytes,
              fromnetscapecolorname, asbytes

.. autoclass:: XYZColor
    :members: x, y, z, alpha

.. autoclass:: YIQColor
    :members: y, i, q, alpha

.. autoclass:: YUVColor
    :members: y, u, v, alpha
