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

::

    class ObjectTestNPC(MapObject):

        def __init__(self):
            MapObject.__init__(self, MapObject.OBSTACLE, image_file='actor1.png',
                               image_index=7)
            self.movement_behavior.movements.extend([Wait(30), ForcedStep(UP),
                                                     Wait(30), ForcedStep(DOWN)])

        def activate(self, party_avatar, direction):
            for i in xrange(2):
                party_avatar.schedule_movement(Step(inverse(direction)))
            party_avatar.schedule_movement(Face(direction))
