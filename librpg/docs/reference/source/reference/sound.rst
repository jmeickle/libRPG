:mod:`sound` -- Music and sound effects
=======================================

.. automodule:: librpg.sound
   :members:
   :show-inheritance:

Usage
-----

To play a background music in a map, simply call MapModel.set_music()
passing the name of the music file as parameter.

To play a sound effect, use play_sfx().

Example
-------

::

    from librpg.sound import play_sfx
    play_sfx('sound6.wav')
    