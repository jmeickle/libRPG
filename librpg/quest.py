class QuestBook(dict):

    """
    """

    def __init__(self, quest_factory, owner):
        """
        """
        dict.__init__(self)
        self.factory = quest_factory
        self.owner = owner

    def add_quest(self, quest_id, *args):
        """
        """
        if quest_id in self.keys():
            # Quest already started
            return False

        quest = self.factory.fabricate(quest_id, *([self.owner] + list(args)))
        self[quest_id] = quest
        quest.book = self
        
        quest.start()

    def get_quests(self):
        return self.values()


class Quest(object):

    """
    """

    def __init__(self, owner, name, steps):
        """
        """
        try:
            self.id
        except AttributeError:
            raise Exception('Classes derived from Quest must have an id as'\
                            'class attribute')

        self.owner = owner
        self.name = name
        self.step = 0
        self.steps = [step_class(owner) for step_class in steps]

    def advance(self):
        """
        """
        self.get_current_step().finish()
        self.step += 1
        if self.is_complete():
            self.custom_complete()
        else:
            self.get_current_step().start()

    def start(self):
        if self.steps:
            self.get_current_step().start()

    def custom_complete(self):
        """
        """
        pass

    def get_current_step(self):
        """
        """
        if self.is_complete():
            return None
        else:
            return self.steps[self.step]

    def is_complete(self):
        """
        """
        return self.step >= len(self.steps)


class QuestStep(object):

    def __init__(self, owner):
        self.owner = owner

    def start(self):
        self.custom_start()

    def finish(self):
        self.custom_finish()

    def custom_finish(self):
        """
        """
        pass

    def custom_start(self):
        """
        """
        pass
