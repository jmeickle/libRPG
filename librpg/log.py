#=================================================================================

class LogRoll:

    UNLIMITED_CAPACITY = -1

    def __init__(self, entry_types, capacity = UNLIMITED_CAPACITY):
        self.capacity = capacity
        self.entry_types = entry_types
        self.entries = []
        self.file = None
    
    def log_to_file(self, file):
        self.file = file
        self.write_to_file(file)
        
    def stop_logging_to_file(self):
        self.file = None
        
    def clean(self):
        self.entries = []
        
    def write(self, entry):
        if self.file != None:
            self.file.write(str(entry) + "\n")
        elif self.capacity == LogRoll.UNLIMITED_CAPACITY or self.capacity > len(self.entries):
            self.entries.append(entry)
        
    def __repr__(self):
        return self.entries.__repr__()
        
    def __str__(self):
        s = ''
        for entry in self.entries:
            s += str(entry) + '\n'
        return s

    def write_to_file(self, file):
        for entry in self.entries:
            file.write(str(entry) + "\n")
        self.clean()

class Log:

    ALL_LOG_ENTRIES = 1
    
    # Contains all Rolls created
    rolls = []
    
    # Maps the entry_types to their list of Rolls
    index = {}
    
    # List of rolls that catch all entries
    rolls_that_catch_all = []

    def create_roll(self, entry_types = ALL_LOG_ENTRIES, capacity = LogRoll.UNLIMITED_CAPACITY):
        roll = LogRoll(entry_types, capacity)
        
        if (entry_types == Log.ALL_LOG_ENTRIES):
            Log.rolls_that_catch_all.append(roll)
        else:
            for entry_type in entry_types:
                if entry_type in Log.index.keys():
                    Log.index[entry_type].append(roll)
                else:
                    Log.index[entry_type] = [roll]
                    
        Log.rolls.append(roll)
        
        return roll
   
   
    def destroy_roll(self, roll):
        Log.rolls.remove(roll)

        if roll.entry_types == Log.ALL_LOG_ENTRIES:
            Log.rolls_that_catch_all.remove(roll)
        else:
            for entry_type in roll.entry_types:
                Log.index[entry_type].remove(roll)
                if len(Log.index[entry_type]) == 0:
                    del Log.index[entry_type]
                    
                    
    def write(self, entry):
        if entry.entry_type in Log.index.keys():
            for roll in Log.index[entry.entry_type]:
                roll.write(entry)
        for roll in Log.rolls_that_catch_all:
            roll.write(entry)
   
class LogEntry:

    def __init__(self, entry_type):
        self.entry_type = entry_type
        if self.entry_type == Log.ALL_LOG_ENTRIES:
            self.repr = "ALL_LOG_ENTRIES"
        else:
            self.repr = entry_type
    
    def __repr__(self):
        return self.repr
        
    def __str__(self):
        return "<LogEntry type:" + self.repr + ">"
        