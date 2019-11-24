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

Rendered Subcomponent
=====================

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
'<ul title="Say Howdy"><li>Hello World</li><li>Hello Universe</li><li>Hello Galaxy</li></ul>'

Let's use that as our foray into some more features.

Real Component
==============

That's not a real component, it's just a Python function call in the middle of an expression.
``htm`` and thus ``htm.py`` support a first-class concept of a component, in the grammar, which gets compiled.

Components have a curly brace around them. Let's do a simple Greeting, but first, without passing an argument:

.. literalinclude:: hp03.py
    :start-after: start

.. invisible-code-block: python

  from hp03 import result03

React popularized having lots of small, reusable, functional components.
Here's how the ``Heading`` renders:

>>> result03
'<header>Hello World</header>'

Component "Props"
=================

JSX uses "props", which are a series of HTML attribute-looking things.
Our ``html`` function is currently acting like a factory.
Let's make it smarter about gathering up props.

.. literalinclude:: hp04.py
    :start-after: start

.. invisible-code-block: python

  from hp04 import result04

Rather than call the "tag" immediately, we instead need to pass the props to a function which will:

- Pick them apart
- Pass them as arguments to the callable at ``tag``
- Return the result

This is the kind of thing factories such as ``html`` are good for.
Here's the result we get:

>>> result04
'<header>Hello My Components</header>'

Argument Sniffing
=================

Our factory does a good job of forwarding along arguments from the "props" to the callable.
But what if the props provide something the callable doesn't want?

Let's make the ``tag_factory`` a little smarter, by having it sniff at the function arguments.
Then, get the requested args from the props before calling:

.. literalinclude:: hp05.py
    :start-after: start

.. invisible-code-block: python

  from hp05 import result05

Note that our usage of ``Heading`` included a prop ``unused`` which is ignored, since we are sniffing the ``Heading`` callable's arguments.
As an additional feature, our ``Heading`` callable doesn't have to ask for ``children`` when it isn't using it.

>>> result05
'<header>Hello My Components</header>'

Lots more features could go in here, such as type coercion.

Component Children
==================

A component might expect to receive some children, which it will then place as it wishes.
Our `tag_factory` supports it, so let's show it:

.. literalinclude:: hp06.py
    :start-after: start

.. invisible-code-block: python

  from hp06 import result06


>>> result06
'<div><header>Hello My Components</header><div>Some children</div></div>'
