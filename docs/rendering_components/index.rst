====================
Rendering Components
====================

Generating the VDOM diffs is the heart of the matter.
VDOM is a well-known, well-regarded technique for performant browser user interfaces.

But how do we apply those diffs to get HTML, especially server-side where we just want a string?
Let's take a look at some patterns that can help our thinking.
Just to be clear, we are still in proof-of-concept mode and doing experimentation.

.. note::

  The VDOM technique is mature and dominant, but other approaches (hyperHTML, Svelte) are showing there are newer, possibly-better ways.

Helper Module
=============

Let's use a helper module to generate the HTML.
This is similar to the `hyperpython Python package <https://hyperpython.readthedocs.io/en/latest/>`_.
Later this might become part of ``htm.py``, or a standalone package, or just supported with ``hyperpython``.

.. literalinclude:: h.py

``h.py`` is the main "library" that implements html for generating the DOM and render for rendering it.

It illustrates some general patterns, such as:

- functional components (see functional_component below)

- generator components (see generator_component below)

- boolean props (see editable in the output)

- components only getting the props they're asking for (via relaxed_call in h.py)

- fragments and nested child lists (via flatten in h.py)

- conditional rendering (True/False/None get ignored - see footer_message below)

For now, it just generates a string, thus is a server-side solution.
Later it could talk to the DOM to do the updating.

Hello World
===========

As we did in basic usage, let's do Hello World, but this time render to a string:

.. literalinclude:: rc1.py

.. invisible-code-block: python

  from rc1 import rc1

The result this time is a string instead of a triple:

>>> rc1
'<div>Hello World</div>'

What's different?
We're still generating a VDOM with ``html`` but we're passing that VDOM to a ``render`` function to get a string.

Dynamic Values
==============

Again, as we did in basic usage, let's do a dynamic Hello World which renders a string:

.. literalinclude:: rc2.py

.. invisible-code-block: python

  from rc2 import rc2

The result this time is a string instead of a triple:

>>> rc2
'<div>Hello World</div>'

Boolean Props
=============

Let's see the first benefit of controlling output... we can handle boolean props:

.. literalinclude:: rc3.py

.. invisible-code-block: python

  from rc3 import rc3

XXX TODO should this output be editable="true" ?

>>> rc3
'<div editable>Hello World</div>'


Functional Components
=====================

React popularized having lots of small, reusable, functional components.
Let's see how that would work:

.. literalinclude:: rc4.py

.. invisible-code-block: python

  from rc4 import rc4

Our output now contains the subcomponent, which uses a value passed in from the caller instead of the default:

>>> rc4
'<h2>My Components</h2>'

Children
========

It's nice to have a "tag", or functional component, that you can re-use simply by passing arguments.
Sometimes, though, the caller has more than just a simple value to pass in... it has nested children that need to be available in the component.

Use the special name ``children`` to access those:

.. literalinclude:: rc5.py

.. invisible-code-block: python

  from rc5 import rc5

Our output now contains the children of the caller, placed in the spot determined by the subcomponent:

>>> rc5
'<h2>My Components</h2><div>Hello World</div>'

Generator Component
===================

Todo lists are popular.
Sometimes you have a lot of todo items and want to use a generator, to save memory.
Meaning, you want a *generator component*:

.. literalinclude:: rc6.py

.. invisible-code-block: python

  from rc6 import rc6

Our output now contains the children of the caller, placed in the spot determined by the subcomponent:

>>> rc6
'<h2>My Todos</h2><ul><li>foo</li><li>bar</li></ul>'

Conditional Rendering
=====================

Maybe you only want a footer when a value is provided:

.. literalinclude:: rc7.py

.. invisible-code-block: python

  from rc7 import rc7

Our output now contains the children of the caller, placed in the spot determined by the subcomponent:

>>> rc7
'<h2>My Todos</h2><ul><li>foo</li><li>bar</li></ul><footer>The Footer</footer>'