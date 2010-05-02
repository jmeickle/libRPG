from librpg.context import Context
from pygame.locals import KEYDOWN


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

    def process_event(self, event):
        if event.type == KEYDOWN:
            command = self.mapping.get(event.key, None)
            if command is not None:
                if hasattr(command, '__getitem__'):
                    return command[0](*command[1:])
                else:
                    return command()
