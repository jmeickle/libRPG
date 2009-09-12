"""
The :mod:`log` module provides a powerful and flexible logging interface.

When the write() function is called, the entry passed as parameter will
be inserted into all LogRolls that were configured to catch that type of
entry. These types are called *entry types*, and are normally strings.

The objects passed to write() should be inherited from LogEntry,
implementing the __str__() method, which should return the string as it
should be printed in the screen or log file.

"""

class LogRoll(object):

    """
    A LogRoll receives all LogEntries that it was configured to catch and
    either stores them or logs them to a file.
    """
    
    UNLIMITED_CAPACITY = -1
    """
    Constant which can be passed to create_roll indicating it has no
    entry count limit.
    """

    def __init__(self, entry_types, capacity=UNLIMITED_CAPACITY):
        """
        *Constructor:*
        
        Initialize the LogRoll to catch the desires entry types
        (*entry_types* should be a list of entry_types) and to contain
        up to *capacity* entries. The default *capacity* is unlimited.
        """
        self.capacity = capacity
        self.entry_types = entry_types
        self.entries = []
        self.logfile = None

    def log_to_file(self, logfile):
        """
        Write all stored entries to the file and any new incoming entries,
        until stop_logging_to_file() is called or log_to_file() passing a
        different file.
        
        *logfile* should be an open *file*.
        """
        self.logfile = logfile
        self.write_to_file(logfile)

    def stop_logging_to_file(self):
        """
        Stop writing to a file, if the LogRoll had executed log_to_file().
        """
        self.logfile = None

    def clean(self):
        """
        Erase all stored entries.
        """
        self.entries = []

    def write(self, entry):
        """
        Store entry or write it immediately to a file.
        """
        if self.logfile is not None:
            self.logfile.write('%s\n' % str(entry))
        elif self.capacity == LogRoll.UNLIMITED_CAPACITY or\
                self.capacity > len(self.entries):
            self.entries.append(entry)

    def __repr__(self):
        return self.entries.__repr__()

    def __str__(self):
        return '\n'.join([str(entry) for entry in self.entries])

    def write_to_file(self, logfile):
        """
        Writes all stored entries to the file but does not write
        subsequently added entries automatically.
        """
        logfile.write(str(self))
        self.clean()

ALL_LOG_ENTRIES = 1
"""
Constant which can be passed to create_roll to have it catch all entries.
"""

# Contains all Rolls created
rolls = []

# Maps the entry_types to their list of Rolls
index = {}

# List of rolls that catch all entries
rolls_that_catch_all = []

def create_roll(entry_types=ALL_LOG_ENTRIES,
                capacity=LogRoll.UNLIMITED_CAPACITY):
    """
    Create a new LogRoll with the specified characteristics and return
    it.
    
    The new LogRoll will catch all entries which entry type is in the
    list *entry_types*. It will be able to hold as many entries as
    *capacity*. By default, it will catch any entry, and have an
    infinite capacity.
    
    """
    roll = LogRoll(entry_types, capacity)

    if (entry_types == ALL_LOG_ENTRIES):
        rolls_that_catch_all.append(roll)
    else:
        for entry_type in entry_types:
            if entry_type in index.keys():
                index[entry_type].append(roll)
            else:
                index[entry_type] = [roll]

    rolls.append(roll)

    return roll


def destroy_roll(roll):
    """
    Destroy a LogRoll.
    
    The LogRoll *roll* will be destroyed, which means it will stop
    catching entries.
    """
    rolls.remove(roll)

    if roll.entry_types == ALL_LOG_ENTRIES:
        rolls_that_catch_all.remove(roll)
    else:
        for entry_type in roll.entry_types:
            index[entry_type].remove(roll)
            if len(index[entry_type]) == 0:
                del index[entry_type]


def write(entry):
    """
    Write a LogEntry to all LogRolls that catch it.
    
    The *entry* will be inserted in all LogRolls created by create_roll
    that passed a list containing the *entry*'s entry type.
    """
    if entry.entry_type in index.keys():
        for roll in index[entry.entry_type]:
            roll.write(entry)
    for roll in rolls_that_catch_all:
        roll.write(entry)


class LogEntry(object):

    """
    A LogEntry is one event to be logged to a LogRoll.
    """
    
    def __init__(self, entry_type):
        self.entry_type = entry_type
        if self.entry_type == ALL_LOG_ENTRIES:
            self.repr = "ALL_LOG_ENTRIES"
        else:
            self.repr = entry_type

    def __repr__(self):
        return self.repr

    def __str__(self):
        """
        *Virtual.* Return a string with how the LogEntry should be written
        to a log file.
        
        """
        return "<LogEntry type: %s>" % self.repr

