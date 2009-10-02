:mod:`camera` -- Cameras for viewing maps
=========================================

.. automodule:: librpg.camera
   :members:
   :show-inheritance:

Usage
-----

To change the camera mode, simply set config.graphics_config.camera_mode
to an instance of the desired camera mode. This can be done by simple
attribution or the config() method.

To create a new camera mode, inherit from CameraMode and override
calc_bg_slice_topleft() and - if necessary - attach_to_map().

Example
-------

::

    librpg.config.graphics_config.camera_mode = librpg.camera.PartyConfinementCameraMode(50, 40)
