""" make .wav files for each not in a blues scale """

def add_note(out, instr, key_num, duration, bpm, volume):
    """ Adds a note from the given instrument to the specified stream

    out: the stream to add the note to
    instr: the instrument that should play the note
    key_num: the piano key number (A 440Hzz is 49)
    duration: the duration of the note in beats
    bpm: the tempo of the music
    volume: the volume of the note
    """
    Wavefile.setDefaults(sampling_rate, 16)
    freq = (2.0**(1/12.0))**(int(key_num)-49)*440.0
    stream = instr.play(duration*(60.0/bpm),freq)
    stream *= volume
    out << stream


from Nsound import *
sampling_rate = 4400.0 #sampling rate for .wav file
Bass = OrganPipe(sampling_rate)    # use an Bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
    See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]

bpm = 45
max_volume = 1

for num, note in enumerate(blues_scale):
    add_note(solo, Bass, note, 1, bpm, max_volume)

    solo >> "blues_note%02d.wav" % num
    solo = AudioStream(sampling_rate, 1)