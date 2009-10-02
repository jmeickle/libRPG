from librpg.quest import *
from librpg.util import IdFactory

quest_factory = IdFactory()

# Quests ###################################################

class TeaAtFiveQuest(Quest):

    id = 'tea at five'

    class Step1(QuestStep):

        def custom_start(self):
            print 'Started Tea at Five step 1'

        def custom_finish(self):
            print 'Finished Tea at Five step 1'
            self.owner.reward(100)

    class Step2(QuestStep):

        def custom_start(self):
            print 'Started Tea at Five step 2'

        def custom_finish(self):
            print 'Finished Tea at Five step 2'
            self.owner.reward(300)

    def __init__(self, owner):
        Quest.__init__(self, owner, 'Tea at Five',
                       [TeaAtFiveQuest.Step1, TeaAtFiveQuest.Step2])

    def custom_complete(self):
        print 'Tea at Five quest completed!'

quest_factory.register(TeaAtFiveQuest)


class JourneyBakeryQuest(Quest):

    id = 'journey bakery'

    def __init__(self, owner):
        Quest.__init__(self, owner, 'Journey to the Bakery', [])

quest_factory.register(JourneyBakeryQuest)


class HousekeepingQuest(Quest):

    id = 'housekeeping'

    def __init__(self, owner):
        Quest.__init__(self, owner, 'Housekeeping', [])

quest_factory.register(HousekeepingQuest)


# Person ###################################################

class Person(object):

    def __init__(self, name):
        self.name = name
        self.book = QuestBook(quest_factory, self)

    def reward(self, xp):
        print '%s earned %d XP!' % (self.name, xp)


# Main #####################################################

if __name__ == '__main__':
    person = Person('Roy')
    book = person.book

    book.add_quest('tea at five')
    book['tea at five'].advance()
    book['tea at five'].advance()
