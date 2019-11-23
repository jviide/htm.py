==============================
Rendering With ``hyperpython``
==============================

As mentioned at the start, ``htm.py`` is only half the equation.
It generates a tree of operations.
For "server side rendering" (SSR), something needs to take that and generate an HTML string.

The `hyperpython <https://hyperpython.readthedocs.io/en/latest/index.html>`_ package can do that.
The output of ``htm.py`` -- the VDOM tree -- is the input to ``hyperpython``.

Let's take a look.

Hello World
===========

In :ref:`bu-hello-world` we saw a snippet that generated the VDOM for a static "Hello World".
Let's re-do it, but with rendering to a string:

.. literalinclude:: hp01.py
    :emphasize-lines: 2, 7, 10

.. invisible-code-block: python

  from hp01 import result01

What's different? We import the `h` function from ``hyperpython`` and have our ``html`` function pass the ``htm`` stuff into it.
Then, we get the string representation at the end, which does the conversion into a string:

As such, instead of a Python tuple of VDOM thingies, we get an HTML string:

>>> result01
'<div>Hello World</div>'

Rendered Component
==================

Let's now recreate another example: :ref:`bu-subcomponents`.
But this time, rendering a string.

.. literalinclude:: hp02.py
    :emphasize-lines: 2, 7, 10
    :start-after: start

.. invisible-code-block: python

  from hp02 import result02

What's different? We import the `h` function from ``hyperpython`` and have our ``html`` function pass the ``htm`` stuff into it.
Then, we get the string representation at the end, which does the conversion into a string.

As such, instead of a Python tuple of VDOM thingies, we get an HTML string:

>>> result02
'<ul title="Say Howdy"><li>Hello World</li><li>Hello Universe</li><li>Hello Galaxy</li></ul>'sph

Let's use that as our foray into some more features.

