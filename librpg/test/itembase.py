from librpg.util import IdFactory
from librpg.item import OrdinaryItem, UsableOrdinaryItem
from librpg.dialog import ChoiceDialog


item_factory = IdFactory()


class LogItem(OrdinaryItem):

    id = 'log'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Log')
item_factory.register(LogItem)


class LeafItem(OrdinaryItem):

    id = 'leaf'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Leaf')
item_factory.register(LeafItem)


class PotionItem(UsableOrdinaryItem):

    id = 'potion'

    def __init__(self):
        UsableOrdinaryItem.__init__(self, 'Potion')

    def use(self, party):
        dialog = ChoiceDialog('Use on whom?', party.chars)
        dialog.sync_open()
        
        target = party.chars[dialog.result]
        print 'Using on %s' % (target)
    
item_factory.register(PotionItem)


class ElixirItem(OrdinaryItem):

    id = 'elixir'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Elixir')
item_factory.register(ElixirItem)


class FeatherItem(OrdinaryItem):

    id = 'feather'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Feather')
item_factory.register(FeatherItem)


class EmptyVialItem(OrdinaryItem):

    id = 'empty vial'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Empty Vial')
item_factory.register(EmptyVialItem)


class LavenderItem(OrdinaryItem):

    id = 'lavender'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Lavender')
item_factory.register(LavenderItem)


class BasilItem(OrdinaryItem):

    id = 'basil'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Basil')
item_factory.register(BasilItem)


class RosemaryItem(OrdinaryItem):

    id = 'rosemary'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Rosemary')
item_factory.register(RosemaryItem)


class FangsItem(OrdinaryItem):

    id = 'fangs'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Fangs')
item_factory.register(FangsItem)
