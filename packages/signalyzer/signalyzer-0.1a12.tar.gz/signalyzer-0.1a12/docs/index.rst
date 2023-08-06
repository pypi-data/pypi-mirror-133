.. currentmodule:: signalyzer

.. _JupyterLab: https://jupyter.org/
.. _numpy: https://numpy.org/
.. _scipy: https://www.scipy.org/
.. _pandas: https://pandas.pydata.org/docs/
.. _plotly: https://plotly.com/python/
.. _dash: https://dash.plotly.com/
.. _voila: https://voila.readthedocs.io/
.. _PyPI package registry: https://gitlab.com/signalytics/signalyzer/-/packages


Welcome to the Signalyzer Documentation
===========================================

Signalyzer is a Python package to analyze time-discrete, equidistant signals,
and visualize them with the open source `Plotly`_ library for Python.

.. important::

  The ``signalyzer`` package is best used within the `JupyterLab`_ web-based
  interactive development environment for Jupyter notebooks or with Plotly
  `Dash`_ or Jupyter `voila`_ to build standalone web applications and dashboards.

Modules
-------

The ``signalyzer`` package comes with two modules.

The :ref:`trace module <signal trace>` for transforming, processing, analyzing
and plotting time-discrete, equidistant signals.

.. note:: The ``signalyzer.trace`` module is imported into the package
  namespace.

The :ref:`statemachine module <statemachine>` for evaluating and plotting state
transitions of a state machine observed by a time-discrete, equidistant signal.

.. note:: The ``signalyzer.statemachine`` module is imported into the
  package namespace.

Dependencies
------------

The Python package runs on `Python 3.9 <https://www.python.org>`_ or higher
and depends on the external packages:

* `numpy`_ for mathematical computations
* `scipy`_ for signal processing and signal statistics computations
* `pandas`_ for data import and statistic computations
* `plotly`_ for visualizations

You can get the latest version from the project `PyPI package registry`_.

.. toctree::
   :caption: Trace
   :maxdepth: 3
   :hidden:

   trace/index
   transformations/index
   collections/index
   processing/index

.. toctree::
   :caption: State Machines
   :maxdepth: 3
   :hidden:

   statemachine/index

.. toctree::
   :maxdepth: 4
   :caption: References
   :hidden:

   api/index

.. toctree::
   :maxdepth: 2
   :caption: Annex
   :hidden:

   annex/changelog
   annex/license
   annex/contributing

.. toctree::
   :maxdepth: 1
   :caption: Indexes
   :hidden:

   genindex
