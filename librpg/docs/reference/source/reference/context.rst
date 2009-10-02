:mod:`context` -- Context Stack mechanism
=========================================

.. automodule:: librpg.context
   :members:
   :show-inheritance:

Usage
-----

Contexts are an advanced part of LibRPG, which, even though should be used
with caution, allow an unlimited set of features that would not be
possible otherwise.

To create a Context, inherit the Context class and override the desired
methods. A (base) Context is basically a process that could do stuff, draw and
capture events, but doesn't. Overriding any of these methods in a derived
class will make it do stuff, draw and/or capture events.

To run a Context, just instantiate it and insert it into the global
ContextStack by calling ContextStack.insert_context() or
ContextStack.stack_context(). This will cause it to be initialized once,
then run every gameloop.

Example
-------

A simple life bar that just draws to the screen over the map::

    class LifeBar(Context):

        def __init__(character, parent=None):
            Context.__init__(parent)
            self.character = character
            
        def draw():
            life_percentage = (float) self.character.life / self.character.max_life
            librpg.virtualscreen.get_screen().blit(self.render(life_percentage),
                                                   (20, 20))
            
        def render(life_percentage):
            # Return a Surface with the image of the life bar
