from music21 import midi, note, stream, chord, duration
from music21.pitch import PitchException
from markov_model import add_chords
import subprocess
import os

rhythms = {
    'q': 1.0,
    '.q': 1.5,
    'w': 4.0,
    'h': 2.0,
    '.h': 3.0,
    '8': 0.5,
    '16': 0.25
}


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.
    """
    piece = stream.Part()
    notes = []

    for item in melody.split():
        try:
            n, d = item.split('\\')
            n = note.Note(n)
            notes.append(n.name)
            dur = duration.Duration(rhythms[d])
            n.duration = dur
            piece.append(n)
        except PitchException:
            piece.append(note.Rest(item))

    return piece, notes


def combine_notes_and_chords(melody, chords):

    accomp = stream.Part()

    for c_notes in chords:
        try:
            c = chord.Chord(c_notes)
        except PitchException:
            c = note.Rest()
        accomp.append(c)

    piece = stream.Stream()
    piece.append(melody)
    piece.append(accomp)

    return piece


def new_song(melody, user_id=''):
    """ Creates a new song from a user input melody.
    """

    path = 'static/user_files/user' + str(user_id) + '/temp/'
    if not os.path.exists(path):
        os.makedirs(path)
    mid = path + 'temp_song.mid'
    wav = path + 'temp_song.wav'

    # turn melody string into music21 object and transpose
    parsed_input, notes = parse_melody(melody)
    chords = add_chords(notes)

    song = combine_notes_and_chords(parsed_input, chords)
    # write to midi file
    mf = midi.translate.streamToMidiFile(song)
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

    os.rename('static/user_files/user' + str(user_id) + '/temp/temp_song.wav', path + filename)


def save_image(path, filename, data):

    if not os.path.exists(path):
        os.makedirs(path)

    image = data[22:]
    missing_padding = len(image) % 4
    if missing_padding != 0:
        image += b'=' * (4 - missing_padding)
    fh = open(path+filename, "wb")
    fh.write(image.decode('base64'))
    fh.close()
