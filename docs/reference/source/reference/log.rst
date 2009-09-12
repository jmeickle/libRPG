:mod:`log` -- Generic logging
=============================

.. automodule:: log
   :members:
   :show-inheritance:

Usage
-----

    - To create a LogRoll, use create_roll() specifying the entry types
      that the roll should catch. To destroy a LogRoll, use destroy_roll().

    - To write a LogEntry to all rolls that catch it, simply call
      write().

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
        
        def __repr__(self):
            return "+" + str(self.n)
            
    class SubtractedEntry(LogEntry):
        def __init__(self, n):
            LogEntry.__init__(self, "SubtractedEntry")
            self.n = n
         
        def __str__(self):
            return "Subtracted " + str(self.n)
        
        def __repr__(self):
            return "-" + str(self.n)
            
    a = create_roll(["AddedEntry"])
    b = create_roll(["SubtractedEntry"])
    c = create_roll(["AddedEntry", "SubtractedEntry"])
    d = create_roll()

    a.log_to_file(file("logtest.added.log", "w"))
    b.log_to_file(file("logtest.subtracted.log", "w"))

    write(AddedEntry(1))
    write(SubtractedEntry(2))
    write(AddedEntry(3))
    write(SubtractedEntry(4))
    write(SubtractedEntry(5))
    write(SubtractedEntry(6))

    c.write_to_file(file("logtest.both.log", "w"))

    write(AddedEntry(7))
    write(AddedEntry(8))

    print d
