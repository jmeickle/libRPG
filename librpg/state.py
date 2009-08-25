from __future__ import with_statement
import pickle

class State(object):

    # Read-Only Attibutes
    # locals - maps feature strings to local states

    def __init__(self, filename=None):
        self.locals = {}
        if filename is not None:
            self.load(filename)

    def load(self, filename):
        with open(filename, "r") as file:
            self.locals = pickle.load(file)

    def save(self, filename):
        with open(filename, "w") as file:
            pickle.dump(self.locals, file)

    def load_local(self, feature):
        return self.locals.get(feature)

    # local_state must be serializable
    def save_local(self, feature, local_state):
        self.locals[feature] = local_state

    def update(self, new_data):
        self.locals.update(new_data)
