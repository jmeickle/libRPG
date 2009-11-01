:mod:`movement` -- Movement management for MapObjects
=====================================================

.. automodule:: librpg.movement
   :members:
   :show-inheritance:

Usage
-----

The two ways to use Movements on a MapObject:

    1) To make the object do the movement once, call MapObject.\
    schedule_movement() passing the instantiated movement. This will make the
    object execute it as soon as the others that are already in progress or
    enqueued finish. 

    2) To give an object a movement routine, inserted them into the
    movement_behavior.movement member of MapObject, which is a list, meaning it
    can be manipulated as such.

Example
-------

**test/objecttest16.py** (fragment)

.. literalinclude:: ../../../../test/objecttest16.py
    :start-after: # movement.rst example starts here
    :end-before: # movement.rst example ends here
