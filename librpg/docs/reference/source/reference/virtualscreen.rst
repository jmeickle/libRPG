:mod:`virtualscreen` -- Screen with scaling
===========================================

.. automodule:: librpg.virtualscreen
   :members:
   :show-inheritance:

Usage
-----

To blit to the screen directly - typically from within a context's draw() method - call get_screen() to get a handle to the ScaledScreen. Use its blit() method like as if it were the display, but don't flip() it, just let the ContextStack do so.
