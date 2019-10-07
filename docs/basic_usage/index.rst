===========
Basic Usage
===========

``htm.py`` advertises itself as a Python implementation of `htm <https://github.com/developit/htm>`_, a JavaScript templating package.
``htm`` advertises itself as a replacement for JSX, a simpler way to do VDOM-compatible templating.

Let's take a look at some of the templating patterns in ``htm.py``.

Hello World
===========

Let's start with generating ``<div>Hello World</div>``.
This is a single node (the ``<div>``) with one child, a text node (``Hello World``.)

Here is a "template", the ``html`` function, which generates the VDOM-like output:

.. literalinclude:: example_01.py

.. invisible-code-block: python

  from example_01 import result01

What is this VDOM-like output?
A series of possibly-nested tuples, as explained in TODO.

>>> result01
('div', {}, ['Hello World'])


Dynamic Values
==============

That was pretty boring...all static, no "templating".
Let's have the template insert a value:


.. literalinclude:: example_02.py
    :start-after: start

.. invisible-code-block: python

  from example_02 import result02

As you can see, we use brackets, as in ``{name}``, to insert values.
The output is just a little be different now:

>>> result02
('div', {}, ['Hello ', 'World'])


Static Attributes
==================

Wonder what the second item -- the empty ``{}`` -- is for in the tuple?
That's where attributes for that node would go.
Let's add an attribute:

.. literalinclude:: example_03.py
    :start-after: start

.. invisible-code-block: python

  from example_03 import result03

This returns:

>>> result03
('div', {'title': 'Say Hi'}, ['Hello ', 'World'])

So now you see the structure of the tuple:

- First item is the tag name

- Second item is for attribute information

- Third item is for child nodes

Dynamic Attributes
===================

Wonder what the second item -- the empty ``{}`` -- is for in the tuple?
That's where attributes for that node would go.
Let's add an attribute:

.. literalinclude:: example_04.py
    :start-after: start

.. invisible-code-block: python

  from example_04 import result04

And the result:

>>> result04
('div', {'title': 'Say Howdy'}, ['Hello ', 'World'])


Nested Children
================

We're dealing with a single node.
But what happens when we have a tree of nodes, which is usually the case?
That's where nesting comes in, and that's where the VDOM approach shines.

.. literalinclude:: example_05.py
    :start-after: start

.. invisible-code-block: python

  from example_05 import result05

The result now has a tuple whose third item -- the children -- is a sequence:

>>> result05
('section', {}, [('div', {'title': 'Say Howdy'}, ['Hello ', 'World'])])

Inline Python
==============

Perhaps we want the ``name`` value in all uppercase?
This "template" language supports Python expressions inside the brackets:

.. literalinclude:: example_06.py
    :start-after: start

.. invisible-code-block: python

  from example_06 import result06

The output is the same, but with ``World`` in all caps:

>>> result06
('section', {}, [('div', {'title': 'Say Howdy'}, ['Hello ', 'WORLD'])])

Looping
=======

Rendering a list of things is very common.
JSX, Jinja2, and most other template-like environments make it easy to do so.
In JSX, you use the language's looping facilities.
Same in ``htm.py``:

.. literalinclude:: example_07.py
    :start-after: start

.. invisible-code-block: python

  from example_07 import result07

What's the output?
The children of ``ul`` -- meaning, the third element of the tuple -- holds a sequence of sequences:

>>> result07
('ul', {'title': 'Say Howdy'}, [[('li', {}, ['Hello ', 'World']), ('li', {}, ['Hello ', 'Universe']), ('li', {}, ['Hello ', 'Galaxy'])]])

Subcomponents
=============

In React and JSX, you frequently split things into lots -- LOTS -- of small, single-focused components.
Let's extract the ``<li>`` into a subcomponent:

.. literalinclude:: example_08.py
    :start-after: start

.. invisible-code-block: python

  from example_08 import result08

The results are the same:

>>> result08
('ul', {'title': 'Say Howdy'}, [[('li', {}, ['Hello ', 'World']), ('li', {}, ['Hello ', 'Universe']), ('li', {}, ['Hello ', 'Galaxy'])]])
