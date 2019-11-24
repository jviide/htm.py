===========
Basic Usage
===========

``htm.py`` advertises itself as a Python implementation of `htm <https://github.com/developit/htm>`_, a JavaScript templating package.
``htm`` advertises itself as a replacement for JSX, a simpler way to do VDOM-compatible templating.

Let's take a look at some of the templating patterns in ``htm.py``.

.. _bu-hello-world:

Hello World
===========

Let's start with generating ``<div>Hello World</div>``.
This is a single node (the ``<div>``) with one child, a text node (``Hello World``.)

Here is a "template", the ``html`` function, which generates the VDOM-like output:

.. literalinclude:: bu01.py

.. invisible-code-block: python

  from bu01 import result01

What is this VDOM-like output?
A series of possibly-nested tuples, as explained in TODO.

>>> result01
('div', {}, ['Hello World'])


Dynamic Values
==============

That was pretty boring...all static, no "templating".
Let's have the template insert a value:


.. literalinclude:: bu02.py
    :start-after: start

.. invisible-code-block: python

  from bu02 import result02

As you can see, we use brackets, as in ``{name}``, to insert values.
The output is just a little be different now:

>>> result02
('div', {}, ['Hello ', 'World'])


Static Attributes
==================

Wonder what the second item -- the empty ``{}`` -- is for in the tuple?
That's where attributes for that node would go.
Let's add an attribute:

.. literalinclude:: bu03.py
    :start-after: start

.. invisible-code-block: python

  from bu03 import result03

This returns:

>>> result03
('div', {'title': 'Say Hi'}, ['Hello ', 'World'])

So now you see the structure of the tuple:

- First item is the tag name

- Second item is for attribute information

- Third item is for child nodes

Dynamic Attributes
===================

Attributes aren't always static, of course.
You can make them dynamic by -- you guessed it -- curly brackets containing an expression:

.. literalinclude:: bu04.py
    :start-after: start

.. invisible-code-block: python

  from bu04 import result04

And the result:

>>> result04
('div', {'title': 'Say Howdy'}, ['Hello ', 'World'])


Nested Children
================

We're dealing with a single node.
But what happens when we have a tree of nodes, which is usually the case?
That's where nesting comes in, and that's where the VDOM approach shines.

.. literalinclude:: bu05.py
    :start-after: start

.. invisible-code-block: python

  from bu05 import result05

The result now has a tuple whose third item -- the children -- is a sequence:

>>> result05
('section', {}, [('div', {'title': 'Say Howdy'}, ['Hello ', 'World'])])

Inline Python
==============

Perhaps we want the ``name`` value in all uppercase?
This "template" language supports Python expressions inside the brackets:

.. literalinclude:: bu06.py
    :start-after: start

.. invisible-code-block: python

  from bu06 import result06

The output is the same, but with ``World`` in all caps:

>>> result06
('section', {}, [('div', {'title': 'Say Howdy'}, ['Hello ', 'WORLD'])])

Looping
=======

Rendering a list of things is very common.
JSX, Jinja2, and most other template-like environments make it easy to do so.
In JSX, you use the language's looping facilities.
Same in ``htm.py``:

.. literalinclude:: bu07.py
    :start-after: start

.. invisible-code-block: python

  from bu07 import result07

What's the output?
The children of ``ul`` -- meaning, the third element of the tuple -- holds a sequence of sequences:

>>> result07
('ul', {'title': 'Say Howdy'}, [[('li', {}, ['Hello ', 'World']), ('li', {}, ['Hello ', 'Universe']), ('li', {}, ['Hello ', 'Galaxy'])]])

.. _bu-subcomponents:

Conditional Rendering
=====================

Maybe you only want a footer when a value is provided:

.. literalinclude:: bu08.py

.. invisible-code-block: python

  from bu08 import result08

Our output now contains the children of the caller, placed in the spot determined by the subcomponent:

>>> result08
[('h1', {}, ['Show?']), 'Say Howdy']

Here's another variation that inserts a subtemplate conditionally:

.. literalinclude:: bu08b.py

.. invisible-code-block: python

  from bu08b import result08b

We now get some richer output:

>>> result08b
('div', {}, [('h1', {}, ['Show?']), ('p', {}, ['Say Howdy'])])

Subcomponents
=============

In React and JSX, you frequently split things into lots -- LOTS -- of small, single-focused components.
Let's extract the ``<li>`` into a subcomponent:

.. literalinclude:: bu09.py
    :start-after: start

.. invisible-code-block: python

  from bu09 import result09

The results are the same:

>>> result09
('ul', {'title': 'Say Howdy'}, [[('li', {}, ['Hello ', 'World']), ('li', {}, ['Hello ', 'Universe']), ('li', {}, ['Hello ', 'Galaxy'])]])
