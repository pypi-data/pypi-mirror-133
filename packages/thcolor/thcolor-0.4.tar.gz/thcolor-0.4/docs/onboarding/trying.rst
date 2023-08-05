Trying out thcolor
==================

Once thcolor is installed, it is time to put it to the test!
Here are a few use cases for the library.

Converting an RGB color to HSL:

.. code-block:: python

	from thcolor.colors import SRGBColor

	color = SRGBColor.frombytes(55, 23, 224)
	print(color.ashsl())

Converting a HSL color to RGB with an alpha value:

.. code-block:: python

	from thcolor.colors import HSLColor
	from thcolor.angles import DegreesAngle

	color = HSLColor(DegreesAngle(180), 0.5, 1.0, 0.75)
	print(color.assrgb())

Converting a textual representation to the RGBA color components:

.. code-block:: python

	from thcolor.colors import Color

	color = Color.fromtext('darker(10%,  hsl(0, 1, 50.0%))')
	print(color.assrgb())

Getting the CSS color representations (with compatibility for earlier CSS
versions) from a textual representation:

.. code-block:: python

	from thcolor.colors import Color

	color = Color.fromtext('gray(red( #123456 )/0.2/)')
	for repres in color.css():
		print(f'color: {repres}')

For more information, please consult the guides, discussion topics and
API reference on the current documentation.
