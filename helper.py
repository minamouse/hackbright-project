from parse_music import parse_melody, to_scale_degrees
from music21 import midi
import fake_markov
import subprocess
import os


def new_song(melody, user_id=''):
    """ Creates a new song from a user input melody.
    """

    mid = 'static/song' + str(user_id) + '.mid'
    wav = 'static/song' + str(user_id) + '.wav'

    # turn melody string into music21 object and transpose
    parsed_input = parse_melody(melody)
    melody = to_scale_degrees(parsed_input)

    new_song, notes, chords = fake_markov.add_chords(melody)

    # write to midi file
    mf = midi.translate.streamToMidiFile(new_song)
    mf.open(mid, 'wb')
    mf.write()
    mf.close()

    # convert to .wav format
    subprocess.call(['timidity ' + mid + ' -Ow -o ' + wav], shell=True)
    return notes, chords


def save_file(path, filename, user_id=None):
    """Given a path name, moves the temporary song.wav file to the given path.
    """

    if not os.path.exists(path):
        os.makedirs(path)

    os.rename('static/song' + str(user_id) + '.wav', path + filename)
