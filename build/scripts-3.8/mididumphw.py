#!/Users/adam.suki1/workspace/python3-midi/venv/bin/python
"""
Print a description of the available devices.
"""
import midi.sequencer as sequencer

s = sequencer.SequencerHardware()

print s
