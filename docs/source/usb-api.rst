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

.. automodule:: pybpod_soundcard_module.utils.generate_sound
    :members:

Usage Example
=============

.. code:: python

    import numpy as np
    from pybpod_soundcard_module.module import SoundCard, SoundCommandType
    from pybpod_soundcard_module.module_api import SoundCardModule, DataType, SampleRate
    from pybpod_soundcard_module.utils.generate_sound import generate_sound

    card = SoundCardModule()
    card.open()

    sound_filename = 'sound.bin'
    sound_index = 4

    # load file and read data (we are using the numpy's fromfile method)
    wave_int = np.fromfile(sound_filename, dtype=np.int32)

    # NOTE: As an alternative, we can generate a sound dynamically with the helper method generate_sound
    wave_int = generate_sound(sound_filename,           # optional, if given, it will save the generated sound to the hard drive
                              fs=96000,                 # sample rate in Hz
                              duration=4,               # duration of the sound in seconds
                              frequency_left=1500,      # frequency of the sinusoidal signal generated in Hz for the left channel
                              frequency_right=1200)     # frequency of the sinusoidal signal generated in Hz for the right channel

    # send sound
    card.send_sound(wave_int,
                    sound_index,
                    SampleRate._96000HZ,
                    DataType.INT32,
                    sound_filename,
                    'sound_metadata.bin',    # optional
                    'sound_description.txt') # optional

    # reads the files related with the sound in index 4, without cleaning the destination folder
    card.read_sounds(output_folder='folder', sound_index=sound_index, clean_dst_folder=False)

    card.close()

Usage Example (using 'with' statement)
======================================

.. code:: python

    import numpy as np
    from pybpod_soundcard_module.module import SoundCard, SoundCommandType
    from pybpod_soundcard_module.module_api import SoundCardModule, DataType, SampleRate
    from pybpod_soundcard_module.utils.generate_sound import generate_sound

    sound_filename = 'sound.bin'
    sound_index = 4

    # load file and read data (we are using the numpy's fromfile method)
    wave_int = np.fromfile(sound_filename, dtype=np.int32)

    # NOTE: As an alternative, we can generate a sound dynamically with the helper method generate_sound
    wave_int = generate_sound(sound_filename,           # optional, if given, it will save the generated sound to the hard drive
                              fs=96000,                 # sample rate in Hz
                              duration=4,               # duration of the sound in seconds
                              frequency_left=1500,      # frequency of the sinusoidal signal generated in Hz for the left channel
                              frequency_right=1200)     # frequency of the sinusoidal signal generated in Hz for the right channel


    # the with statement will call 'close' automatically at the end of the block
    with SoundCardModule() as card:
        # send sound
        card.send_sound(wave_int,
                        sound_index,
                        SampleRate._96000HZ,
                        DataType.INT32,
                        sound_filename,
                        'sound_metadata.bin',    # optional
                        'sound_description.txt') # optional

        # reads the files related with the sound in index 4 without cleaning the destination folder
        card.read_sounds(output_folder='folder', sound_index=4, clean_dst_folder=False)
