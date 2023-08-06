===========
ColourAlpha
===========

Converts and manipulates common color representation (RGB, HSL, web, ...)

This project is forked from `Colour <https://github.com/vaab/colour/>`_.

Features
========

- Damn simple and pythonic way to manipulate color representation (see
  examples below)

- Full conversion between RGB, HSL, 6-digit hex, 3-digit hex, human color

- One object (``Color``) or bunch of single purpose function (``rgb2hex``,
  ``hsl2rgb`` ...)

- ``web`` format that use the smallest representation between
  6-digit (e.g. ``#fa3b2c``), 3-digit (e.g. ``#fbb``), fully spelled
  color (e.g. ``white``), following `W3C color naming`_ for compatible
  CSS or HTML color specifications.

- smooth intuitive color scale generation choosing N color gradients.

- can pick colors for you to identify objects of your application.


.. _W3C color naming: http://www.w3.org/TR/css3-color/#svg-color


Installation
============

You don't need to download the GIT version of the code as ``colouralpha`` is
available on the PyPI. So you should be able to run:

.. code-block::

    pip install colouralpha

If you have downloaded the GIT sources, then you could add the ``colour.py``
directly to one of your ``site-packages`` (thanks to a symlink). Or install
the current version via:

.. code-block::

    poetry install

And if you don't have the GIT sources but would like to get the latest
main or branch from gitlab, you could also:

.. code-block::

    pip install git+https://gitlab.com/marcin-serwin/colouralpha.git

Or even select a specific revision (branch/tag/commit):

.. code-block::

    pip install git+https://gitlab.com/marcin-serwin/colouralpha.git@main


Usage
=====

To get complete demo of each function, please read the source code which is
heavily documented and provide a lot of examples in doctest format.

You may also access generated documentation `here <https://colouralpha.readthedocs.io/en/latest/>`_.

Here is a reduced sample of a common usage scenario:


Instantiation
-------------

Let's create blue color:

.. code-block:: python

    >>> from colour import Color
    >>> c = Color("blue")
    >>> c
    <Color blue>

Please note that all of these are equivalent examples to create the red color:

.. code-block:: python

    Color("red")           ## human, web compatible representation
    Color(red=1)           ## default amount of blue and green is 0.0
    Color("blue", hue=0)   ## hue of blue is 0.66, hue of red is 0.0
    Color("#f00")          ## standard 3 hex digit web compatible representation
    Color("#ff0000")       ## standard 6 hex digit web compatible representation
    Color(hue=0, saturation=1, luminance=0.5)
    Color(hsl=(0, 1, 0.5)) ## full 3-uple HSL specification
    Color(rgb=(1, 0, 0))   ## full 3-uple RGB specification
    Color(Color("red"))    ## recursion doesn't break object


Reading values
--------------

Several representations are accessible:

.. code-block:: python

    >>> c.hex
    '#00f'
    >>> c.hsl  # doctest: +ELLIPSIS
    (0.66..., 1.0, 0.5)
    >>> c.rgb
    (0.0, 0.0, 1.0)

And their different parts are also independently accessible, as the different
amount of red, blue, green, in the RGB format:

.. code-block:: python

    >>> c.red
    0.0
    >>> c.blue
    1.0
    >>> c.green
    0.0

Or the hue, saturation and luminance of the HSL representation:

.. code-block:: python

    >>> c.hue  # doctest: +ELLIPSIS
    0.66...
    >>> c.saturation
    1.0
    >>> c.luminance
    0.5

A note on the ``.hex`` property, it'll return the smallest valid value
when possible. If you are only interested by the long value, use
``.hex_l``:

.. code-block:: python

    >>> c.hex_l
    '#0000ff'


Modifying color objects
-----------------------

All of these properties are read/write, so let's add some red to this color:

.. code-block:: python

    >>> c.red = 1
    >>> c
    <Color magenta>

We might want to de-saturate this color:

.. code-block:: python

    >>> c.saturation = 0.5
    >>> c
    <Color #bf40bf>

And of course, the string conversion will give the web representation which is
human, or 3-digit, or 6-digit hex representation depending which is usable:

.. code-block:: python

    >>> "%s" % c
    '#bf40bf'

    >>> c.luminance = 1
    >>> "%s" % c
    'white'


Ranges of colors
----------------

You can get some color scale of variation between two ``Color`` objects quite
easily. Here, is the color scale of the rainbow between red and blue:

.. code-block:: python

    >>> red = Color("red")
    >>> blue = Color("blue")
    >>> list(red.range_to(blue, 5))
    [<Color red>, <Color yellow>, <Color lime>, <Color cyan>, <Color blue>]

Or the different amount of gray between black and white:

.. code-block:: python

    >>> black = Color("black")
    >>> white = Color("white")
    >>> list(black.range_to(white, 6))
    [<Color black>, <Color #333>, <Color #666>, <Color #999>, <Color #ccc>, <Color white>]


If you have to create graphical representation with color scale
between red and green ('lime' color is full green):

.. code-block:: python

    >>> lime = Color("lime")
    >>> list(red.range_to(lime, 5))
    [<Color red>, <Color #ff7f00>, <Color yellow>, <Color chartreuse>, <Color lime>]

Notice how naturally, the yellow is displayed in human format and in
the middle of the scale. And that the quite unusual (but compatible)
'chartreuse' color specification has been used in place of the
hexadecimal representation.


Color comparison
----------------

Sane default
~~~~~~~~~~~~

Color comparison is a vast subject. However, it might seem quite straightforward for
you. ``Colour`` uses a configurable default way of comparing color that might suit
your needs:

.. code-block:: python

    >>> Color("red") == Color("#f00") == Color("blue", hue=0)
    True

The default comparison algorithm focuses only on the "web" representation which is
equivalent to comparing the long hex representation (e.g. #FF0000) or to be more
specific, it is equivalent to compare the amount of red, green, and blue composition
of the RGB representation, each of these value being quantized to a 256 value scale.

This default comparison is a practical and convenient way to measure the actual
color equivalence on your screen, or in your video card memory.

But this comparison wouldn't make the difference between a black red, and a
black blue, which both are black:

.. code-block:: python

   >>> black_red = Color("red", luminance=0)
   >>> black_blue = Color("blue", luminance=0)

   >>> black_red == black_blue
   True


Customization
~~~~~~~~~~~~~

But, this is not the sole way to compare two colors. As I'm quite lazy, I'm providing
you a way to customize it to your needs. Thus:

.. code-block:: python

   >>> from colour import RGB_equivalence, HSL_equivalence
   >>> Color.equality = staticmethod(HSL_equivalence)
   >>> black_red = Color("red", luminance=0)
   >>> black_blue = Color("blue", luminance=0)

   >>> black_red == black_blue
   False

You may also set it per instance:

.. code-block:: python

   >>> black_red = Color("red", luminance=0, equality=HSL_equivalence)
   >>> black_blue = Color("blue", luminance=0, equality=HSL_equivalence)

   >>> black_red == black_blue
   False

As you might have already guessed, the sane default is ``RGB_equivalence``, so:

.. code-block:: python

   >>> Color.equality = staticmethod(RGB_equivalence)
   >>> black_red = Color("red", luminance=0)
   >>> black_blue = Color("blue", luminance=0)

   >>> black_red == black_blue
   True

Here's how you could implement your unique comparison function:

.. code-block:: python

   >>> saturation_equivalence = lambda c1, c2: c1.saturation == c2.saturation
   >>> red = Color("red", equality=saturation_equivalence)
   >>> blue = Color("blue", equality=saturation_equivalence)
   >>> white = Color("white", equality=saturation_equivalence)

   >>> red == blue
   True
   >>> white == red
   False

Note: When comparing 2 colors with equality set per instance, *only* the 
equality function *of the first color will be used*. Thus:

.. code-block:: python

   >>> black_red = Color("red", luminance=0, equality=RGB_equivalence)
   >>> black_blue = Color("blue", luminance=0, equality=HSL_equivalence)

   >>> black_red == black_blue
   True

But reverse operation is not equivalent !:

.. code-block:: python

   >>> black_blue == black_red
   False


Equality to non-Colour objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As a side note, whatever your custom equality function is, it won't be
used if you compare to anything else than a ``Colour`` instance:

.. code-block:: python

    >>> red = Color("red", equality=lambda c1, c2: True)
    >>> blue = Color("blue", equality=lambda c1, c2: True)

Note that these instances would compare as equal to any other color:

.. code-block:: python

    >>> red == blue
    True

But on another non-Colour object:

.. code-block:: python

    >>> red == None
    False
    >>> red != None
    True

Actually, ``Colour`` instances will, politely enough, leave
the other side of the equality have a chance to decide of the output,
(by executing its own ``__eq__``), so:

.. code-block:: python

    >>> class OtherColorImplem(object):
    ...     def __init__(self, color):
    ...         self.color = color
    ...     def __eq__(self, other):
    ...         return self.color == other.web

    >>> alien_red = OtherColorImplem("red")
    >>> red == alien_red
    True
    >>> blue == alien_red
    False

And inequality (using ``__ne__``) are also polite:

.. code-block:: python

    >>> class AnotherColorImplem(OtherColorImplem):
    ...     def __ne__(self, other):
    ...         return self.color != other.web

    >>> new_alien_red = AnotherColorImplem("red")
    >>> red != new_alien_red
    False
    >>> blue != new_alien_red
    True


Picking arbitrary color for a python object
-------------------------------------------

Basic Usage
~~~~~~~~~~~

Sometimes, you just want to pick a color for an object in your application
often to visually identify this object. Thus, the picked color should be the
same for same objects, and different for different object:

.. code-block:: python

    >>> foo = object()
    >>> bar = object()

    >>> Color(pick_for=foo)  # doctest: +ELLIPSIS
    <Color ...>
    >>> Color(pick_for=foo) == Color(pick_for=foo)
    True
    >>> Color(pick_for=foo) == Color(pick_for=bar)
    False

Of course, although there's a tiny probability that different strings yield the
same color, most of the time, different inputs will produce different colors.

Advanced Usage
~~~~~~~~~~~~~~

You can customize your color picking algorithm by providing a ``picker``. A
``picker`` is a callable that takes an object, and returns something that can
be instantiated as a color by ``Color``:

.. code-block:: python

    >>> my_picker = lambda obj: "red" if isinstance(obj, int) else "blue"
    >>> Color(pick_for=3, picker=my_picker, pick_key=None)
    <Color red>
    >>> Color(pick_for="foo", picker=my_picker, pick_key=None)
    <Color blue>

You might want to use a particular picker, but enforce how the picker will
identify two object as the same (or not). So there's a ``pick_key`` attribute
that is provided and defaults as equivalent of ``hash`` method and if hash is
not supported by your object, it'll default to the ``str`` of your object salted
with the class name.

Thus:

.. code-block:: python

    >>> class MyObj(str): pass
    >>> my_obj_color = Color(pick_for=MyObj("foo"))
    >>> my_str_color = Color(pick_for="foo")
    >>> my_obj_color == my_str_color
    False

Please make sure your object is hashable or "stringable" before using the
``RGB_color_picker`` picking mechanism or provide another color picker. Nearly
all python object are hashable by default so this shouldn't be an issue (e.g. 
instances of ``object`` and subclasses are hashable).

Neither ``hash`` nor ``str`` are perfect solution. So feel free to use
``pick_key`` at ``Color`` instantiation time to set your way to identify
objects, for instance:

.. code-block:: python

    >>> a = object()
    >>> b = object()
    >>> Color(pick_for=a, pick_key=id) == Color(pick_for=b, pick_key=id)
    False

When choosing a pick key, you should closely consider if you want your color
to be consistent between runs (this is NOT the case with the last example),
or consistent with the content of your object if it is a mutable object.

Default value of ``pick_key`` and ``picker`` ensures that the same color will
be attributed to same object between different run on different computer for
most python object.


Color factory
-------------

As you might have noticed, there are few attributes that you might want to see
attached to all of your colors as ``equality`` for equality comparison support,
or ``picker``, ``pick_key`` to configure your object color picker.

You can create a customized ``Color`` factory thanks to the ``make_color_factory``:

.. code-block:: python

    >>> from colour import make_color_factory, HSL_equivalence, RGB_color_picker

    >>> get_color = make_color_factory(
    ...    equality=HSL_equivalence,
    ...    picker=RGB_color_picker,
    ...    pick_key=str,
    ... )

All color created thanks to ``CustomColor`` class instead of the default one
would get the specified attributes by default:

.. code-block:: python

    >>> black_red = get_color("red", luminance=0)
    >>> black_blue = get_color("blue", luminance=0)

Of course, these are always instances of ``Color`` class:

.. code-block:: python

    >>> isinstance(black_red, Color)
    True

Equality was changed from normal defaults, so:

.. code-block:: python

    >>> black_red == black_blue
    False

This because the default equivalence of ``Color`` was set to
``HSL_equivalence``.


Contributing
============

Any suggestion or issue is welcome. Push request are very welcome,
please check out the guidelines.


Push Request Guidelines
-----------------------

You can send any code. I'll look at it and will integrate it myself in
the code base and leave you as the author. This process can take time and
it'll take less time if you follow the following guidelines:

- check your code with PEP8 or pylint. Try to stick to 80 columns wide.
- separate your commits per smallest concern.
- each commit should pass the tests (to allow easy bisect)
- each functionality/bugfix commit should contain the code, tests,
  and doc.
- prior minor commit with typographic or code cosmetic changes are
  very welcome. These should be tagged in their commit summary with
  ``!minor``.
- the commit message should follow gitchangelog rules (check the git
  log to get examples)
- if the commit fixes an issue or finished the implementation of a
  feature, please mention it in the summary.

If you have some questions about guidelines which is not answered here,
please check the current ``git log``, you might find previous commit that
would show you how to deal with your issue.


License
=======

Current license
---------------

Copyright (c) 2022 Marcin Serwin.

Licensed under `BSD License <https://gitlab.com/marcin-serwin/colouralpha/-/blob/main/LICENSE/>`_.

Original license
----------------

The project was forked from `Colour <https://github.com/vaab/colour/>`__. 

Copyright (c) 2012-2017 Valentin Lab.

Licensed under the `BSD License <https://gitlab.com/marcin-serwin/colouralpha/-/blob/main/LICENSE.old>`__.
