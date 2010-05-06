from librpg.context import Context
from librpg.input import Input


class CommandContext(Context):

    """
    A Context that captures key presses and executes commands bound to
    them.

    *mapping* should be a dict that maps pygame keys to callbacks
    (without parameters) that will be called upon that key press.
    The callback should return False if the event is captured,
    False otherwise.
    """

    def __init__(self, mapping, parent=None):
        Context.__init__(self, parent)
        self.mapping = mapping

    def update(self):
        for key, command in self.mapping.iteritems():
            if Input.down_unset(key) is not None:
                if hasattr(command, '__getitem__'):
                    return command[0](*command[1:])
                else:
                    return command()
