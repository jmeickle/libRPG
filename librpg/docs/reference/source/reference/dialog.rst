:mod:`dialog` -- Simple dialogs
===============================

.. automodule:: librpg.dialog
   :members:
   :show-inheritance:

Usage
-----

To display a Dialog, instantiate it and call the MapModel.schedule_message() method passing the Dialog.

Example
-------

::

    class ObjectTestNPC(MapObject):

        def __init__(self):
        
            MapObject.__init__(self, MapObject.OBSTACLE, image_file='actor1.png',
                               image_index=7)
            self.movement_behavior.movements.extend([Wait(30), ForcedStep(UP),
                                                     Wait(30), ForcedStep(DOWN)])
            
        def activate(self, party_avatar, direction):
        
            print 'Activated NPC'
            for i in xrange(2):
                party_avatar.schedule_movement(Step(inverse(direction)))
            party_avatar.schedule_movement(Face(direction))
            self.map.schedule_message(MessageDialog(u"Ouch!", block_movement=False))
            self.map.schedule_message(MessageDialog(u"Hey, why are you hitting me?",
                                                    block_movement=False))
            self.map.schedule_message(ChoiceDialog(u"Choose NOW:",
                                                   ["choice 1", "choice 2"],
                                                   block_movement=False))
