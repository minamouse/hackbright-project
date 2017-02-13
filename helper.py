from parse_music import parse_melody, to_scale_degrees
import fake_markov
import subprocess
from music21 import midi
import os


def new_song(melody, user_id=None):
    """ Creates a new song from a user input melody.
    """

    # just to be safe, if the files already exist, they will be deleted
    subprocess.call(['rm static/song.mid'], shell=True)
    subprocess.call(['rm static/song.wav'], shell=True)

    # turn melody string into music21 object and transpose
    parsed_input = parse_melody(melody)
    melody = to_scale_degrees(parsed_input)

    new_song = fake_markov.add_chords(melody)

    # write to midi file
    mf = midi.translate.streamToMidiFile(new_song)
    mf.open('static/song.mid', 'wb')
    mf.write()
    mf.close()

    # convert to .wav format
    subprocess.call(['timidity static/song.mid -Ow -o static/song.wav'], shell=True)
    return True


def save_file(path, filename):
    """Given a path name, moves the temporary song.wav file to the given path.
    """

    if not os.path.exists(path):
        os.makedirs(path)

    command = 'mv static/song.wav ' + path + filename
    subprocess.call([command], shell=True)
