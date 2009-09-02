"""
The :mod:`party` module provides functions to manage character groups
and pools of characters that can be picked to join a group.
"""

import pygame

from librpg.image import ObjectImage
from librpg.locals import *

def default_party_factory(reserve):
    return Party(reserve)

class Party(object):

    """
    A Party is a group of Characters that move together in a map.
    """

    def __init__(self, reserve):
        """
        Initialize a party that takes characters from a CharacterReserve.
        
        :attr:`capacity`
            Maximum number of characters in the Party.

        :attr:`reserve`
            CharacterReserve that contains the party's characters

        :attr:`chars`
            List of characters in the party currently

        :attr:`leader`
            Character whose image will be displayed in the map.

        :attr:`avatar`
            PartyAvatar that represents the party in the map.
        """
        self.reserve = reserve
        self.chars = []
        self.leader = None
        self.avatar = None
        reserve.register_party(self)

    def initial_state(self, capacity, chars=None, leader=None):
        """
        Put the Party in an initial configuration without loading its
        state from a save.

        *capacity* should be an integer with the maximum number of
        Characters the party can hold.

        *chars*, should be a list of the names of the initial characters.

        *leader* should be the name of the initial leader. By default the
        party is empty.
        """
        self.capacity = capacity
        self.chars = []
        self.leader = None
        if chars is not None:
            for char in chars:
                self.add_char(char)
        if leader is not None:
            self.leader = leader
        self.custom_init()
        
    def add_char(self, name):
        """
        Insert a Character in the Party.

        *name* should be the character's name.

        Return True is the character was added, False if the operation
        failed, which happens either because the Character already was
        in the Party or because it is already full.
        """
        if (name not in self.reserve.get_names()
            or len(self.chars) >= self.capacity):
            return False
        else:
            self.reserve._allocate_char(name, self)
            self.chars.append(name)
            if self.leader is None:
                self.set_leader(name)
            return True

    def remove_char(self, name):
        """
        Remove a Character from the Party.

        *name* should be the character's name.

        Return True is the character was removed, False if the operation
        failed because the Character was not found in the party.
        """
        if name in self.chars:
            self.reserve._allocate_char(name, None)
            self.chars.remove(name)
            if self.leader == name:
                if len(self.chars) == 0:
                    self.set_leader(None)
                else:
                    self.set_leader(self.chars[0])
            return True
        else:
            return False

    def destroy(self):
        """
        Return a Party's characters to an available state.
        """
        self.reserve._destroy_party(self)

    def empty(self):
        """
        Return whether the party is empty.
        """
        return len(self.chars) == 0

    def __repr__(self):
        if len(self.chars) == 0:
            return '(Empty party)'
        else:
            chars = ', '.join([str(c) for c in self.chars if c != self.leader])
            return '(Leader: %s, %s)' % (self.leader, chars)

    def get_char(self, name):
        """
        Return the Character instance of the character with the given
        name.
        """
        if name not in self.chars:
            return None
        else:
            return self.reserve.get_char(name)

    def get_image(self, avatar):
        """
        Return the image to represent the Party on the map.
        
        *avatar* does not need to be specified, unless a class derived from
        Party wants to have an image that depends on it and overloads
        this function.
        """
        assert self.leader is not None, 'A Party with no characters may not be \
                                        displayed'
        return self.get_char(self.leader).image

    def save_state(self):
        return ((self.capacity, self.chars, self.leader),
                self.custom_save())

    def custom_save(self):
        """
        *Virtual.*
        
        Return a serializable local state to store the party's
        information.
        """
        return None

    def load_state(self, party_state):
        """
        Load the party setup from *party_state*.
        """
        data = party_state[0]
        self.capacity = data[0]
        self.chars = data[1]
        self.set_leader(data[2])
        
        self.custom_load(party_state[1])

    def custom_load(self, party_state):
        """
        *Virtual.*
        
        Initialize whatever fields depend on the state that was saved in a
        previous game.

        *party_state* is the local state returned by save_state() when the state
        was saved.
        """
        pass

    def custom_init(self):
        """
        *Virtual.*
        
        Initial config whatever attributes would be normally loaded from
        a save file.

        This is the analogous to Party.custom_load() for initial_state
        case rather than load_state.
        """
        pass

    def set_leader(self, new_leader):
        self.leader = new_leader
        if self.avatar is not None:
            self.avatar.reload_image()


class CharacterReserve(object):

    """
    A CharacterReserve is a container for characters that can be used
    in Parties.
    """

    def __init__(self, character_factory,
                 party_factory=default_party_factory):
        """
        *Constructor.*
        
        *character_factory* that, given a character name, returns an
        instance of that character.
        
        *party_factory* should be a factory function that returns an
        instance of Party or some derived class, given a reserve. This
        defaults to the base Party constructor.

        :attr:`chars`
            Dict mapping character names to the Characters in the reserve.

        :attr:`party_allocation`
            Dict mapping character names in the reserve to the Party each
            of them is in.

        :attr:`parties`
            List of Parties created by this reserve.

        :attr:`character_factory`
            Factory function that, given a name, returns an instance of
            the related character.

        :attr:`party_factory`
            Factory function that returns an instance of Party or some
            derived class, given a reserve. This defaults to the base
            Party constructor.
        """
        self.chars = {}
        self.party_allocation = {}
        self.parties = []
        self.character_factory = character_factory
        self.party_factory = party_factory

    def add_char(self, name, char_state=None):
        """
        Add a Character to the reserve.
        
        *name* should be the character's name. If the character is
        supposed to be newly crated, *char_state* should be None.
        If it is being loaded, *char_state* should be a serializable
        with the necessary data.
        """
        self.chars[name] = self.character_factory(name)
        if char_state is not None:
            self.chars[name].load_state(char_state)
        else:
            self.chars[name].initial_state()
        self.party_allocation[name] = None

    def remove_char(self, name):
        """
        Remove a character from the reserve.
        
        *name* should be the character's name.
        
        Return the Character if he was in the reserve, None otherwise.
        """
        if self.chars.has_key(name):
            char = self.chars[name]
            if self.party_allocation[name] is not None:
                self.party_allocation[name].remove_char(name)
            del self.chars[name]
            del self.party_allocation[name]
            return char
        else:
            return None

    def register_party(self, party):
        self.parties.append(party)
        for char in party.chars:
            self._allocate_char(char, party)

    def _destroy_party(self, party):
        assert party in self.parties, 'Trying to destroy a Party not in this \
                                       reserve'
        for char in party.chars:
            self._allocate_char(char, None)
        self.parties.remove(party)

    def _allocate_char(self, name, party):
        assert name in self.get_names(), 'Character is not in reserve'
        assert party is None or party in self.parties, 'Party is not in reserve'
        self.party_allocation[name] = party

    def set_default_party(self, party):
        self.parties.remove(party)
        self.parties.insert(0, party)

    def get_default_party(self):
        if self.parties:
            return self.parties[0]
        else:
            return None

    def get_char(self, name):
        """
        Return the Character mapped to *name* in the reserve.

        None is returned if no character with that name was found.
        """
        return self.chars.get(name, None)

    def get_names(self):
        """
        Return a list of the character names in the reserve.
        """
        return self.chars.keys()

    def get_chars(self):
        """
        Return a list of the Characters in the reserve.
        """
        return self.chars.values()

    def __repr__(self):
        return self.party_allocation.__repr__()

    def save_state(self):
        # Save characters
        result = {}
        result[CHARACTERS_LOCAL_STATE] = {}
        for char in self.get_chars():
            result[CHARACTERS_LOCAL_STATE][char.name] = char.save_state()

        # Save parties
        result[PARTIES_LOCAL_STATE] = []
        for party in self.parties:
            result[PARTIES_LOCAL_STATE].append(party.save_state())
        return result
    
    def load_state(self, state):
        assert state.has_key(CHARACTERS_LOCAL_STATE), 'State does not have '\
               'character information.'
        assert state.has_key(CHARACTERS_LOCAL_STATE), 'State does not have '\
               'party information.'
        for name, char_state in state[CHARACTERS_LOCAL_STATE].iteritems():
            self.add_char(name, char_state)
        for party_state in state[PARTIES_LOCAL_STATE]:
            party = self.party_factory(self)
            party.load_state(party_state)

    def initial_state(self, chars=[]):
        for char in chars:
            self.add_char(char)


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
            Must be unique.

        :attr:`image_file`
            Name of the file with the character's sprites.

        :attr:`image`
            ObjectImage with the character's sprites.
        """
        self.name = name
        self.image_file = image_file
        if image_file:
            self.image = ObjectImage(self.image_file, index)
        else:
            self.image = None

    def __repr__(self):
        return self.name

    def save_state(self):
        return (self.name, self.custom_save())

    def custom_save(self):
        """
        *Virtual.*
        
        Return a serializable local state to store the character's
        information.
        """
        return None

    def initial_state(self):
        pass

    def load_state(self, char_state):
        # do_nothing(char_state[0]), maybe in the future.
        self.custom_load(char_state[1])

    def custom_load(self, char_state=None):
        """
        *Virtual.*
        
        Initialize whatever fields depend on the state that was saved in a
        previous game.

        *char_state* is the local state returned by custom_save() when the
        state was saved.
        """
        pass
