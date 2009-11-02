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

**test/objecttest.py** (fragment)

.. literalinclude:: ../../../../test/objecttest.py
    :pyobject: ObjectTestChest
