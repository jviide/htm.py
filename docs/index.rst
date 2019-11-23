=======
html.py
=======

*Powerful, composable, performant, convenient, Python-centric templating.*

Looking for a more modern, Python-centric templating approach that resembles frontend solutions like JSX?
``htm.py`` is a Python implementation of `htm <https://github.com/developit/htm>`_.
With ``htm.py`` you use an f-string-like value with native Python expressions to generate a virtual DOM (VDOM) data structure,
then pass it to a compatible renderer for generating strings of markup.

``htm.py`` tracks the syntax and features of ``htm`` (JS), so if you like ``htm``, you'll like ``htm.py``.
Since Python's f-strings don't match JavaScript's tagged templates, ``htm.py`` uses the companion package `tagged <https://github.com/jviide/tagged>`_ as a bridge.

.. note::

  ``htm.py`` is the *first* half of generating HTML.
  It generates a structural representation.
  To get from that, to an HTML string, you feed ``htm.py``'s "VDOM" output into a *renderer*, such as  `hyperpython <https://hyperpython.readthedocs.io/en/latest/>`_ or a custom renderer.
  These docs give examples of both.

.. image:: https://user-images.githubusercontent.com/19776768/59420458-99d60000-8dd5-11e9-9d29-02fff6c83a55.png

Installation
============

.. code-block:: bash

    $ pip3 install htm

Usage
=====

.. code-block:: python

    from htm import htm

    @htm
    def html(tag, props, children):
        return tag, props, children

    a = 1
    b = {"bar": 100}
    c = "span"
    d = "world"

    html("""
      <div foo={a+2} ...{b}>
        <{c}>Hello, {d}!<//>
      </div>
    """)
    # ('div', {'foo': 3, 'bar': 100}, [('span', {}, ['Hello,', 'world', '!'])])

Development
===========

Running Tests
-------------

.. code-block:: shell

    $ python3 -m unittest discover -s tests

Building Docs
-------------

Documentation is available in the `docs` directory.
First install the dependencies then build the docs:

.. code-block:: shell

    $ pip install -e .[docs]
    $ cd docs
    $ sphinx-build -b html . _build

License
=======

This library is licensed under the MIT license. See [./LICENSE](./LICENSE).

Contents
========

.. toctree::
    :maxdepth: 1

    basic_usage/index
    rendering_components/index

Indices and tables
==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
