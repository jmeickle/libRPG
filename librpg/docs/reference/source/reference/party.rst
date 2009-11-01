:mod:`party` -- Party and Character management
==============================================

.. automodule:: librpg.party
   :members:
   :show-inheritance:

Usage
-----

Characters are created normally by instantiating the Character class. A
name and an image for the Character must be provided.

Parties are always bonded to a CharacterReserve and take its members from
that reserve. To create a CharacterReserve, simply instantiate it. To add
Characters to that reserve, use CharacterReserve.add_char(), or pass a list
of those Characters to CharacterReserve's constructor.

To create a Party, instantiate it passing the world's CharacterReserve
(world.reserve).

To add characters to a party, use the Party.add_char() method. To remove them,
use Party.remove_char().

To destroy a Party, use the Party.destroy() method, which will return the
Characters in the Party to an available state.

Example
-------

**test/partytest.py**

.. literalinclude:: ../../../../test/partytest.py
