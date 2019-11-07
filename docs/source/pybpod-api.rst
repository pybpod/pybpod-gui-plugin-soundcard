*************************************
:mod:`PyBpod SoundCard module API`
*************************************

.. autoclass:: pybpod_soundcard_module.module.SoundCommandType
    :members:

.. autoclass:: pybpod_soundcard_module.module.SoundCard
    :members:
    :private-members:
    :show-inheritance:

Usage Example
=============

.. code:: python

    from pybpodapi.protocol import Bpod, StateMachine
    from pybpod_soundcard_module.module import SoundCard, SoundCommandType

    # sound index to play
    sound_index = 2
    my_bpod = Bpod(serial_port='/dev/ttyACM0')

    # get first SoundBoard module connected to a Bpod serial port
    sound_module = [x for x in my_bpod.modules if x.name == 'SoundCard1'][0]
    sound_module_play = 1

    card = (SoundCard)(sound_module)

    # define serial message to be used in the states with the sound_module_play id
    my_bpod.load_serial_message(sound_module, sound_module_play,
                         card.get_command(SoundCommandType.PLAY, sound_index))

    sma = StateMachine(my_bpod)

    sma.add_state(
        state_name='myState',
        state_timer=2,
        state_change_conditions={Bpod.Events.Tup: 'myState2'},
        output_actions=[(Bpod.OutputChannels.Serial1, sound_module_play)])

    sma.add_state(
        state_name='myState2',
        state_timer=3,
        state_change_conditions={Bpod.Events.Tup: 'exit'},
        output_actions=[(Bpod.OutputChannels.Serial1, card.get_command(SoundCommandType.STOP_ALL))])

    my_bpod.send_state_machine(sma)

    my_bpod.run_state_machine(sma)

    print("Current trial info: {0}".format(my_bpod.session.current_trial))

    my_bpod.close()
