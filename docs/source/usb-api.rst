*************************************
:mod:`SoundCard USB connection`
*************************************

.. module:: pybpodapi
   :synopsis: top-level module

.. autoclass:: pybpod_soundcard_module.module_api.SampleRate
    :members:
    :private-members:

.. autoclass:: pybpod_soundcard_module.module_api.DataType
    :members:

.. autoclass:: pybpod_soundcard_module.module_api.SoundCardModule
    :members:

Usage Example
=============

.. code:: python
    import numpy as np
    from pybpod_soundcard_module.module import SoundCard, SoundCommandType, DataType, SampleRate

    card = SoundCardModule()
    card.open()

    # load file and read data (we are using the numpy's fromfile method)
    wave_int = np.fromfile(sound_filename, dtype=np.int32)

    # send sound
    card.send_sound(wave_int, 
                    sound_index, 
                    SampleRate._96000Hz, 
                    DataType.Int32, 
                    'sound_bin', 
                    'metadata_filename',    # optional 
                    'description_filename') # optional

    # reads the files related with the sound in index 3, without cleaning the destination folder
    card.read_sounds(output_folder='folder', sound_index=3, clean_dst_folder=False)


    card.close()

Usage Example (using 'with' statement)
======================================

.. code:: python
    import numpy as np
    from pybpod_soundcard_module.module import SoundCard, SoundCommandType
    from pybpod_soundcard_module.module_api import DataType, SampleRate

    # load file and read data (we are using the numpy's fromfile method)
    wave_int = np.fromfile(sound_filename, dtype=np.int32)

    # the with statement will call 'close' automatically at the end of the block
    with SoundCardModule() as card:
        # send sound
        card.send_sound(wave_int, 
                        sound_index, 
                        SampleRate._96000Hz, 
                        DataType.Int32, 
                        'sound_bin', 
                        'metadata_filename',    # optional 
                        'description_filename') # optional

        # reads the files related with the sound in index 3, without cleaning the destination folder
        card.read_sounds(output_folder='folder', sound_index=3, clean_dst_folder=False)

