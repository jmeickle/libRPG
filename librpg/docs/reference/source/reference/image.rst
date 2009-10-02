:mod:`image` -- Image loading and slicing
=========================================

.. automodule:: librpg.image
   :members:
   :show-inheritance:

Usage
-----

Generally, TileImage and Image will not be used by end users.

Using ObjectImage, however, is important when the walking animation should
be different from the default one. This allows weird creatures or injured
people to walk in a convincing way, or objects to have complex and smooth
animations.

Example
-------

::

    class ObjectTestNPC(MapObject):

        def __init__(self):
            MapObject.__init__(self,
                               MapObject.OBSTACLE,
                               image_file='chara1.png',
                               basic_animation=[[0, 0, 1], [0, 1], [2, 1]])
            for dir in [LEFT, DOWN, RIGHT, UP]:
                self.movement_behavior.movements.extend([Wait(30), ForcedStep(dir)])
