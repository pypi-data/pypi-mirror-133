.. _defining-decoders:

Defining a decoder
==================

The goal of this guide is to bootstrap you into making your own color decoder
using tools from thcolor. For clarity, you should first read :ref:`expr`,
especially the :ref:`explain-decoders` section.

For this guide, we will want to do the following:

* Create our ``TutorialColorDecoder`` with extended hexadecimal color
  support.
* Create a ``sum`` function which can take 2 to 5 numbers and sum them.
* Create a ``diff`` function which takes 2 numbers and return the first one
  minus the second one.
* Create a ``reverse_diff`` which takes 2 numbers and return the second one
  minus the first one.
* Create an ``transparent`` function which returns the alpha value
  as a byte between 0 and 255, and returns the transparent color when
  used as a value.
* Create a ``awesome-color`` constant which evaluates as blue.

Setting up the framework
------------------------

First of, the elements you will want to import are the following:

* :py:class:`thcolor.decoders.MetaColorDecoder`, which will be the base
  class your decoder will inherit from.
* :py:class:`thcolor.decoders.alias`, which will be useful when you want to
  define an alias for an existing function without doing it manually.
* :py:class:`thcolor.decoders.fallback`, which will be useful when you want
  to define a fallback value for a given function.
* Colors we might want to use from :py:mod:`thcolor.colors`.
* Angles we might want to use from :py:mod:`thcolor.angles`.

For our exercise, we are going to use :py:class:`thcolor.colors.SRGBColor`
and no angles.

Our base code is the following:

.. code-block:: python

    from thcolor.decoders import MetaColorDecoder, alias, fallback
    from thcolor.colors import Color, SRGBColor

    __all__ = ['TutorialColorDecoder']

    class TutorialColorDecoder(MetaColorDecoder):
        pass

As we want extended hexadecimal colors to be read as well, we need to define
the corresponding option. As described in
:py:class:`thcolor.decoders.ColorDecoder`, the option for doing this is
``__extended_hex_support__``, which gives the following class definition:

.. code-block::

    class TutorialColorDecoder(MetaColorDecoder):
        __extended_hex_support__ = True

Defining the ``sum`` function
-----------------------------

As described in the constraints, the ``sum`` function will sum 2 to 5
numbers; the type of these numbers is not given, so we have three options:

* If the hint on these numbers is ``int``, only integers will be accepted
  by the function, and floats with decimal parts will throw an error.
* If the hint on these numbers is ``float``, integers will be converted
  to ``float`` before being passed on to the function.
* If the hint on these numbers is ``typing.Union[int, float]``, the
  function will receive both depending on what the syntax was in the
  original expression.

Here, for simplicity, we choose to use ``float``. The resulting code is
the following:

.. code-block::

    class TutorialColorDecoder(MetaColorDecoder):
        # ...

        def sum(
            a: float, b: float, c: float = 0,
            d: float = 0, e: float = 0,
        ) -> float:
            return a + b + c + d + e

Defining the ``diff`` and ``reverse_diff`` functions
----------------------------------------------------

As described in the constraints, the ``diff`` function will compute the
difference between two numbers. Based on what we've learned in the previous
function, we can do the following:

.. code-block::

    class TutorialColorDecoder(MetaColorDecoder):
        # ...

        def diff(a: float, b: float) -> float:
            return a - b

Now for the ``reverse_diff`` function, we could define it independently,
but in order to save time, we will use :py:class:`thcolor.decoders.alias`.
This function takes the following arguments:

* The name of the function to alias.
* The new order of the arguments, by name.

Based on this information, the :py:class:`thcolor.decoders.MetaColorDecoder`
will create the function out of the previous function (by calling it) and
take all related annotations and default values (if possible and available).

For our current case, we can define our function the following way:

.. code-block::

    class TutorialColorDecoder(MetaColorDecoder):
        # ...

        reverse_diff = alias('diff', args=('b', 'a'))

Note that aliases can be defined anywhere within the class, even before
the aliased function.

Defining the ``transparent`` function with a fallback value
-----------------------------------------------------------

For the ``transparent`` function, we will get the alpha value, multiply it
by 255 and round it to the nearest integer. However, how do we add a fallback
value for the function? :py:class:`thcolor.decoders.fallback` comes to
our rescue!

Once our function is defined, we use :py:class:`thcolor.decoders.fallback`
as a decorator by giving it the value the function should fall back on when
used as a constant.

The resulting code is the following:

.. code-block::

    class TutorialColorDecoder(MetaColorDecoder):
        # ...

        @fallback(SRGBColor(0, 0, 0, 0.0))
        def transparent(color: Color) -> int:
            return int(round(color.alpha * 255))

Defining the ``awesome-color`` constant
---------------------------------------

For defining a constant, we can use affectations, as for aliases.
But how do we define names with carets when they are illegal in Python names?
We can replace it with ``_``; the color decoders in thcolor are not only
case-insensitive, they also treat carets and underscores the same.

We can thus do the following:

.. code-block::

    class TutorialColorDecoder(MetaColorDecoder):
        # ...

        awesome_color = SRGBColor.frombytes(0, 0, 255)

Testing the resulting class
---------------------------

Putting all of our efforts together, we should have the following code:

.. code-block:: python

    from thcolor.decoders import MetaColorDecoder, alias, fallback
    from thcolor.colors import Color, SRGBColor

    __all__ = ['TutorialColorDecoder']

    class TutorialColorDecoder(MetaColorDecoder):
        __extended_hex_support__ = True

        def sum(
            a: float, b: float, c: float = 0,
            d: float = 0, e: float = 0,
        ) -> float:
            return a + b + c + d + e

        def diff(a: float, b: float) -> float:
            return a - b

        reverse_diff = alias('diff', args=('b', 'a'))

        @fallback(SRGBColor(0, 0, 0, 0.0))
        def transparent(color: Color) -> int:
            return int(round(color.alpha * 255))

        awesome_color = SRGBColor.frombytes(0, 0, 255)

Now that our class is defined, we can instanciate and test our decoder:

.. code-block:: python

    decoder = TutorialColorDecoder()
    results = decoder.decode(
        'awesome-color '
        'sum(sum(1, 2, 3, 4), reverse_diff(transparent(transparent), 4))',
    )

    print(results)

And the result we obtain are the following:

::

    (SRGBColor(red=0.0, green=0.0, blue=1.0, alpha=1.0), 14.0)
