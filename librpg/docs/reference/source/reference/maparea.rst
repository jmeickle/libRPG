:mod:`maparea` -- Map areas
===========================

.. automodule:: librpg.maparea
   :members:
   :show-inheritance:

Usage
-----

MapAreas are typically created and placed on the map during its initialize() routine. They may also be created and placed as a result of some event, during the map's execution.

To create a MapArea, write a class that inherits from it (say, MyArea), overloading some of its callbacks (party_entered(), party_moved(), party_left()). To place it on a map, instantiate it and use map.add_area(), passing a PositionList or any object inherited from PositionList, such as RectangleArea.

Example
-------

::

    class AreaAroundWell(MapArea):

        def party_entered(self, party_avatar, position):
            print 'party_entered(%s, %s)' % (party_avatar, position)

        def party_moved(self, party_avatar, left_position, entered_position,
                        from_outside):
            print 'party_moved(%s, %s, %s, %s)' % (party_avatar, left_position,
                                                   entered_position, from_outside)

        def party_left(self, party_avatar, position):
            print 'party_left(%s, %s)' % (party_avatar, position)

    class Map2(WorldMap):

        def __init__(self):
            WorldMap.__init__(self, 'worldtest/map2.map',
                              ('lower_tileset32.png', 'lower_tileset32.bnd'),
                              [('upper_tileset32.png', 'upper_tileset32.bnd'),])

        def initialize(self, local_state):
            self.add_area(AreaAroundWell(), RectangleArea((2, 3), (4, 5)))
