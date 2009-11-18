from librpg.util import IdFactory
from librpg.item import OrdinaryItem


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
