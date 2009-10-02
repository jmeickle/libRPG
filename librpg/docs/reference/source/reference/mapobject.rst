:mod:`mapobject` -- Map interactive objects
===========================================

.. automodule:: librpg.mapobject
   :members:
   :show-inheritance:

Usage
-----

MapObjects are typically created and placed on the map during its initialize() routine. They may also be created and placed as a result of some event, during the map execution.

To create a MapObject, write a class that inherits from it (say, MyObject), overloading its activate() method. To place it on a map, instantiate it and use map.add_object().

To create a MapObject that takes its image from the scenario tileset, that is, a ScenarioMapObject, inherit from ScenarioMapObject and use it like any MapObject.

- To define the object's movement behavior, append Movement objects to the *movement_behavior.movements* list.
- To define the object's behavior when activated, implement the *activate()* method.
- To define the object's behavior when collided, implement the *collide_with_party()* method.

To have a MapObject be updated every cycle, define an update() method for it and it will be called every map cycle.

Example
-------

::

    class ObjectTestChest(MapObject):

        def __init__(self):
            MapObject.__init__(self, MapObject.OBSTACLE, image_file='chest2.png',
                               image_index=5, facing=UP)
            self.closed = True
            self.filled = True
            
        def activate(self, party_avatar, direction):
            if self.closed:
                self.closed = False
                self.schedule_movement(Face(RIGHT))
                self.schedule_movement(Wait(2))
                self.schedule_movement(Face(DOWN))
                self.schedule_movement(Wait(2))
                self.schedule_movement(Face(LEFT))
                self.map.sync_movement([self])
                if self.filled:
                    print 'Opened chest and added item'
                    self.map.schedule_message(MessageDialog(u"You got Hookshot!"))
                    self.filled = False
                else:
                    print 'Opened chest but it was empty'
                    self.map.schedule_message(MessageDialog(u"The chest is empty\
                                                            =("))
            else:
                print 'Chest is open, closing'
                self.schedule_movement(Face(UP))
                self.closed = True  