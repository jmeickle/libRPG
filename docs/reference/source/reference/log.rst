:mod:`log` -- Generic logging
=============================

.. automodule:: log
   :members:
   :show-inheritance:

Usage
-----

    - Do not instantiate Log, it is a class with only static attributes and
      methods.

    - To create a LogRoll, use Log.create_roll() specifying the entry types
      that the roll should catch. To destroy a LogRoll, use destroy_roll().

    - To write a LogEntry to all rolls that catch it, simply call
      Log.write().

    - To create a LogRoll, call Log.create_roll() passing a list of all
      entry types the roll should catch. To destroy it, call
      Log.destroy_roll().

    - To write entries to the roll, let Log.write() do it automatically to
      all rolls that catch those entries.

    - To write the contents of a LogRoll to a file, use log_to_file() or
      write_to_file(). If you used log_to_file(), the entries received will
      keep being written to that file until stop_logging_to_file() is called.
    
    - To use LogEntries, an entry class should be inherited from LogEntry
      (such as MyEntry). The constructor of that class should pass the class
      name to LogEntry's constructor (LogEntry.__init__(self, "MyEntry")).
      It should also overload __str__() a function that returns the LogEntry
      as it should be printed to a file or to the screen.
      
Example
-------

::

    from librpg.log import *

    class AddedEntry (LogEntry):
        def __init__(self, n):
            LogEntry.__init__(self, "AddedEntry")
            self.n = n
         
        def __str__(self):
            return "Added " + str(self.n)
        
    class SubtractedEntry(LogEntry):
        def __init__(self, n):
            LogEntry.__init__(self, "SubtractedEntry")
            self.n = n
         
        def __str__(self):
            return "Subtracted " + str(self.n)
        
    a = Log().create_roll(["AddedEntry"])
    b = Log().create_roll(["SubtractedEntry"])
    c = Log().create_roll(["AddedEntry", "SubtractedEntry"])
    d = Log().create_roll()

    a.log_to_file(file("logtest.added.log", "w"))
    b.log_to_file(file("logtest.subtracted.log", "w"))

    Log().write(AddedEntry(1))
    Log().write(SubtractedEntry(2))
    Log().write(AddedEntry(3))
    Log().write(SubtractedEntry(4))
    Log().write(SubtractedEntry(5))
    Log().write(SubtractedEntry(6))

    c.write_to_file(file("logtest.both.log", "w"))

    Log().write(AddedEntry(7))
    Log().write(AddedEntry(8))
