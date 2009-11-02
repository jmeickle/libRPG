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

**test/worldtest/mymaps.py** (fragment)

.. literalinclude:: ../../../../test/worldtest/mymaps.py
    :pyobject: AreaAroundWell

.. literalinclude:: ../../../../test/worldtest/mymaps.py
    :pyobject: Map2
