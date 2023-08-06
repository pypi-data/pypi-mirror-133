.. currentmodule:: signalyzer

.. testsetup:: *

    from signalyzer import *

Shifting Functions
==================

.. _move:

Move
----

You can move the signal :attr:`~Trace.samples` by a *number* of samples to the
right by calling the method :func:`~Trace.move` with the positive *number* of
samples the signal :attr:`~Trace.samples` shall be moved to the right.

A new :class:`Trace` instance *labeled* with the performed transformation
``'move'`` is returned.

  >>> # move samples by the number of samples to the right
  >>> Trace('Signal', [1, 2, 3, 4, 5]).move(2)
  Trace(label='Signal:move', samples=[1, 1, 1, 2, 3])

.. note:: The first signal sample is used as the *fill* value to move the signal
  samples to the right.

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [1, 2, 3, 4, 5])
  trace = signal.move(2)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])

You can move the signal :attr:`~Trace.samples` by a *number* of samples to the
left by calling the method :func:`~Trace.move` with the negative *number* of
samples the signal :attr:`~Trace.samples` shall be moved to the left.

A new :class:`Trace` instance *labeled* with the performed transformation
``'move'`` is returned.

  >>> # move samples by the number of samples to the left
  >>> Trace('Signal', [1, 2, 3, 4, 5]).move(-2)
  Trace(label='Signal:move', samples=[3, 4, 5, 5, 5])

.. note:: The last signal sample is used as the *fill* value to move the signal
  samples to the left.

.. plotly::

  import math
  from signalyzer import Trace

  signal = Trace('Signal', [1, 2, 3, 4, 5])
  trace = signal.move(-2)
  go.Figure([signal.plot(), trace.plot(mode='lines+markers')])
