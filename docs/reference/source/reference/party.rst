:mod:`party` -- Party and Character management
==============================================

.. automodule:: party
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

To create a Party, use the CharacterReserve.create_party() method.

To add characters to a party, use the Party.add_char() method. To remove them,
use Party.remove_char().

To destroy a Party, use the CharacterReserve.destroy_party() method, which
will return the Characters in the Party to 

Example
-------

::
    reserve = CharacterReserve()

    reserve.add_char(Character('Andy', 'andy.png'))
    reserve.add_char(Character('Bernie', 'bernie.png'))
    reserve.add_char(Character('Chris', 'chris.png'))
    reserve.add_char(Character('Dylan', 'dylan.png'))
    reserve.add_char(Character('Emma', 'emma.png'))
    
    chars = reserve.get_chars()
    
    party = reserve.create_party(3)
    party.add_char(chars[0])
    party.add_char(chars[2])
    party.add_char(chars[3])
