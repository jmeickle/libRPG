:mod:`world` -- Game world
==========================

.. automodule:: librpg.world
   :members:
   :show-inheritance:

Usage
-----

A World is necessary for any game that makes full use of LibRPG.

For tiny games than only need one map:
   
    1. Instantiate the MapModel corresponding to that map.
    2. Instantiate a MicroWorld passing that MapModel.
    3. Call MicroWorld.initial_state() passing the starting position and characters.
    4. Call the MicroWorld's gameloop().
   
For games that need more than one map:

    1. Define your WorldMaps, inheriting a class from it for each map.
    2. Instantiate the World. As parameter, pass a dict attributing a unique map id to each WorldMap-inherited class.
    3. Call World.initial_state(), passing the starting map id, the starting position and the characters.
    4. Call the World's gameloop().

After a world's gameloop ends, to quit the program it is good to call exit(). This will terminate pygame gracefully.

Note: to load from a save, in step 3 call load_state() instead, passing the name of the save file.


MicroWorld Example
------------------

**test/bouldertest.py**

.. literalinclude:: ../../../../test/bouldertest.py


MacroWorld Example
------------------

**test/worldtest.py**

.. literalinclude:: ../../../../test/worldtest.py


**test/worldtest/myworld.py**

.. literalinclude:: ../../../../test/worldtest/myworld.py


**test/worldtest/mymaps.py**

.. literalinclude:: ../../../../test/worldtest/mymaps.py
