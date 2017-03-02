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

rhythms_back = {0.25: '16',
                1.0: 'q',
                2.0: 'h',
                3.0: 'hd',
                4.0: 'w',
                0.5: '8',
                1.5: 'qd'}


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.
    """
    piece = stream.Part()

    for item in melody:

        dur = duration.Duration(item[1])

        if item[0] != 'r':
            n = note.Note(item[0])
        else:
            n = note.Rest()

        n.duration = dur
        piece.append(n)

    return piece


def combine_notes_and_chords(notes, chords):

    piece = stream.Stream()
    piece.append(notes)
    piece.append(chords)
    return piece


def make_chords(chords, lengths):

    accomp = stream.Part()

    for i in range(len(chords)):
        try:
            c = chord.Chord(chords[i]).closedPosition(forceOctave=3)
            d = duration.Duration(lengths[i])
            c.duration = d
        except PitchException:
            c = note.Rest()
            d = duration.Duration(lengths[i])
            c.duration = d
        accomp.append(c)

    return accomp


def get_measures(melody, accomp):

    melody_measures = melody.makeMeasures()
    accomp_measures = accomp.makeMeasures()

    melody_measure_notes = []
    accomp_measure_notes = []

    for measure in melody_measures:
        this_measure = []
        for n in measure.notesAndRests:
            if type(n) == note.Note:
                this_measure.append((n.nameWithOctave, rhythms_back[n.duration.quarterLength]))
            elif type(n) == note.Rest:
                this_measure.append(('r', n.duration))

        melody_measure_notes.append(this_measure)

    for measure in accomp_measures:
        this_measure = []
        for n in measure.notesAndRests:
            if type(n) == chord.Chord:
                this_measure.append(([p.nameWithOctave for p in n.pitches], rhythms_back[n.duration.quarterLength]))

        accomp_measure_notes.append(this_measure)

    print melody_measure_notes
    print accomp_measure_notes
    return melody_measure_notes, accomp_measure_notes


def new_song(melody, user_id=''):
    """ Creates a new song from a user input melody.
    """

    path = 'static/user_files/user' + str(user_id) + '/temp/'
    if not os.path.exists(path):
        os.makedirs(path)
    mid = path + 'temp_song.mid'
    wav = path + 'temp_song.wav'

    new_melody = []

    for item in melody.split():
        n, d = item.split('\\')
        new_melody.append((n, rhythms[d]))

    parsed_input = parse_melody(new_melody)
    chords, lengths = add_chords(new_melody)

    accomp = make_chords(chords, lengths)

    note_measures, chord_measures = get_measures(parsed_input, accomp)

    song = combine_notes_and_chords(parsed_input, accomp)

    # write to midi file
    mf = midi.translate.streamToMidiFile(song)
    mf.open(mid, 'wb')
    mf.write()
    mf.close()

    # convert to .wav format
    subprocess.call(['timidity ' + mid + ' -Ow -o ' + wav], shell=True)
    return note_measures, chord_measures


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


def validate_input(melody):

    return True
