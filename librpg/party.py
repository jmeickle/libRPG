"""
The :mod:`party` module provides functions to manage character groups
and pools of characters that can be picked to join a group.
"""

import pygame

from image import ObjectImage

class Party(object):

    """
    A Party is a group of Characters that move together in a map.
    """

    def __init__(self, capacity, reserve):
        """
        Do not call the Party constructor directly. Parties should be
        created by the factory method CharacterReserve.create_party().

        :attr:`capacity`
            Maximum number of characters in the Party.

        :attr:`reserve`
            CharacterReserve that contains the party's characters

        :attr:`chars`
            List of characters in the party currently

        :attr:`leader`
            Character whose image will be displayed in the map.
        """
        self.capacity = capacity
        self.reserve = reserve
        self.chars = []
        self.leader = None

    def add_char(self, char):
        """
        Insert a Character in the Party.
        
        Return True is the character was added, False if the operation
        failed, which happens either because the Character already was
        in the Party or because it is already full.
        """
        if char not in self.reserve.get_chars() or\
           len(self.chars) >= self.capacity:
            return False
        else:
            self.reserve.allocate_char(char, self)
            self.chars.append(char)
            if self.leader is None:
                self.leader = char
            return True

    def remove_char(self, char):
        """
        Remove a Character from the Party.
        
        Return True is the character was removed, False if the operation
        failed because the Character was not found in the party.
        """
        if char in self.chars:
            self.reserve.allocate_char(char, None)
            self.chars.remove(char)
            if self.leader == char:
                if len(self.chars) == 0:
                    self.leader = None
                else:
                    self.leader = self.chars[0]
            return True
        else:
            return False

    def __repr__(self):
        if len(self.chars) == 0:
            return '(Empty party)'
        else:
            chars = ', '.join([str(c) for c in self.chars if c != self.leader])
            return '(Leader: %s, %s)' % (self.leader, chars)

    def get_image(self, avatar):
        """
        Returns the image to represent the Party on the map.
        """
        assert self.leader, 'A Party with no characters may not be displayed'
        return self.leader.image


class CharacterReserve(object):

    """
    A CharacterReserve is a container for characters that can be used
    in Parties.
    
    
    """
    # Read-Only Attributes:
    # chars - maps the characters in the reserve currently to the party they are in
    # parties - list of parties that contain the characters in this reserve

    def __init__(self, chars=[]):
        """
        *Constructor.*
        
        To create an empty reserve, do not pass any arguments to the
        constructor. If *chars* is passed as a list of Characters,
        the CharacterReserve will initially contain those Characters.

        :attr:`chars`
            Dict mapping the Characters in the reserve to the Party each
            of them is in.
            
        :attr:`parties`
            List of Parties created by this reserve.
        """
        self.chars = {}
        self.parties = []

        for char in chars:
            self.add_char(char)

    def add_char(self, char):
        """
        Add a Character to the reserve.
        """
        self.chars[char] = None

    def remove_char(self, char):
        """
        Remove a character from the reserve.
        
        Return the Character if he was in the reserve, None otherwise.
        """
        if self.chars.has_key(char):
            if self.chars[char] is not None:
                self.chars[char].remove_char(char)
            del self.chars[char]
            return char
        else:
            return None

    def create_party(self, capacity, chars=[]):
        """
        Create a new Party with the given *capacity* and including
        the Characters passed in the list *chars*.
        """
        party = Party(capacity, self)
        self.parties.append(party)

        for char in chars:
            party.add_char(char)

        return party

    def destroy_party(self, party):
        """
        Destroy a Party, returning its characters to a free state.
        
        Return False if *party* had not been created from this reserve.
        Return True if it was successfully destroyed.
        """
        if party not in self.parties:
            return False
        for char in party.chars:
            self.chars[char] = None
        self.parties.remove(party)
        return True

    def get_chars(self):
        """
        Return a list of the Characters in the reserve.
        """
        return self.chars.keys()

    # Used only by Party
    def allocate_char(self, char, party):
        self.chars[char] = party

    def __repr__(self):
        return self.chars.__repr__()


class Character(object):

    """
    A Character is a person that composes player controlled parties.
    
    Typically Characters will walk in maps organized in parties - 
    possibly a 1-Character party -, engage in battle and so on. They
    can be removed and added to parties. Typically parties have a
    limited number of Characters, such that only a couple can be picked
    from the CharacterReserve.
    """

    def __init__(self, name, image_file=None, index=0):
        """
        *Constructor.*
        
        Specify the *name* of the character, the name of the *image_file*
        where the character's sprites are, and the *index* by which the
        sprites can be found in the object image file.

        :attr:`name`
            A string with the character's *name* as it should be displayed.

        :attr:`image_file`
            Name of the file with the character's sprites.

        :attr:`image`
            ObjectImage with the character's sprites.
        """
        self.name, self.image_file = name, image_file
        if image_file:
            self.image = ObjectImage(self.image_file, index)
        else:
            self.image = None

    def __repr__(self):
        return self.name

