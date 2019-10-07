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

Hello World
===========

As we did in basic usage, let's do Hello World, but this time generate a string:

.. literalinclude:: rc1.py
    :start-after: start

.. invisible-code-block: python

  from rc1 import rc1

The result this time is a string instead of a triple:

>>> rc1
'<div>Hello World</div>'

Callable Components
====================

*Note: This part requires installation of the ``hyperpython`` package.*

We can go a step further and have something that looks a bit more like components.
Along the way, we can more easily handle cases with children, so as when they should be called.
We'll do both with a smarter ``html`` tag function:
