:mod:`map` -- Map core
======================

.. automodule:: map
   :members:
   
Usage
-----

To use a map, three things must be done:

1) Create a .map file with the layout of that map. Pass this file's name to the MapModel constructor.
2) Define the tileset that will be used for drawing the map's terrain and scenario layers. Pass the image and boundaries files' names to the MapModel constructor.
3) Write a class that inherits from MapModel (for example MyMapModel), overriding only the initialize() method with a routine that places the objects and area of the map to an initial state.

When this is done, create a world and insert that MapModel into it. The way this is done depends on the world created:

- In case of a MicroWorld - which is a world with a single map -, instantiate the MapModel and pass it as parameter to the MicroWorld constructor, along with the Party::

    MicroWorld(MyMapModel(), party, Position(1, 2))

- In case of a World - which allows any amount of maps -, first define a unique map_id for that map. Pass it inside the *maps* parameter of the constructor, as a value associated to its map_id as key::

    class MyWorld(World):
        def __init__(self):
            World.__init__(self,
                           maps={1: MyMapModel},
                           initial_map=1,
                           initial_position=Position(1, 2))
    
Then, with the world created, call its gameloop() method.

To add and remove objects from the map, use add_object() and remove_object(). To add and remove areas, use add_area() and remove_area().

Examples
--------
