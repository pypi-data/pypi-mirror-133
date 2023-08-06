.. -*- rst -*- -*- restructuredtext -*-
.. Note: this file is simplified without text roles so it displays on PyPI. See
.. doc/README.rst for the correct information.
   
==================
zopeext for Sphinx
==================

:author: Michael McNeil Forbes <mforbes@alum.mit.edu>

This extension provides an `autointerface` directive for `Zope interfaces`_.

Requirements
============

* Sphinx_: ``pip install sphinx``
* zope.interface_: ``pip install zope.interface``
* sphinxcontrib.zopeext_: ``pip install sphinxcontrib-zopeext``

Usage
=====

In the `build configuration file`_ (the ``conf.py`` in your Sphinx_
documentation directory) add `sphinxcontrib.zopeext.autointerface` to your
``extensions`` list::

   extensions = [..., 'sphinxcontrib.zopeext.autointerface', ...]


Then, in your documentation, use `autointerface` as you would use
`autoclass`.  You can refer to the interface with the ``:py:interface:`` role
`example.IMyInterface` as you would use the ``:py:class:`` role to refer
to the implementation `example.MyImplementation`:

.. code-block:: ReST

    .. automodule:: example
       :show-inheritance:
       :inherited-members:
     
One can also limit which members are displayed, just as you would with ``.. autoclass``:

.. code-block:: ReST

    .. autointerface:: example.IMyInterface
       :members: x, equals
    .. autoclass:: example.MyImplementation
       :members: x, equals

.. _Sphinx: http://sphinx.pocoo.org/
.. _build configuration file: http://sphinx.pocoo.org/config.html
.. _Zope interfaces: http://docs.zope.org/zope.interface/README.html
.. _zope.interface: http://pypi.python.org/pypi/zope.interface/
.. _sphinxcontrib.zopeext: http://pypi.python.org/pypi/sphinxcontrib-zopeext/


..
   """
   Documentation: http://packages.python.org/sphinxcontrib-zopeext

   Install with ``pip install sphinxcontrib-zopeext``.

   To use this extension, include `'sphinxcontrib.zopeext.autointerface'` in your
   `extensions` list in the `conf.py` file for your documentation.

   This provides some support for Zope interfaces by providing an `autointerface`
   directive that acts like `autoclass` except uses the Zope interface methods for
   attribute and method lookup (the interface mechanism hides the attributes and
   method so the usual `autoclass` directive fails.)  Interfaces are intended
   to be very different beasts than regular python classes, and as a result
   require customized access to documentation, signatures etc.

   tests_require = [
       'Sphinx>=3.3.0',
       'sphinx-testing',
       'pytest>=2.8.1',
       'pytest-cov>=2.2.0',
       'pytest-flake8',
       'coverage',
       'flake8',
       'pep8',

   """
