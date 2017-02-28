from music21 import midi, note, stream, chord
from music21.pitch import PitchException
from gnaive_bayes import add_chords
import subprocess
import os


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.
    """
    piece = stream.Part()
    numbers = []
    notes = []

    for item in melody.split():
        try:
            n = note.Note(item)
            piece.append(n)
            numbers.append(n.pitch.midi % 12)
            notes.append(n.nameWithOctave)
        except PitchException:
            piece.append(note.Rest(item))
            numbers.append(12)
            notes.append('r')

    return piece, numbers, notes


# def transpose_back(piece, key):

#     current_note = piece.analyze('key')
#     current_note = note.Note(current_note.name[0])

#     goal_note = note.Note(key.name[0])

#     transpose_intvl = interval.notesToInterval(current_note, goal_note)
#     transposed_piece = piece.transpose(transpose_intvl)

#     notes = []
#     for note1 in transposed_piece[0]:
#         notes.append(note1.nameWithOctave)

#     chords = []

#     for chord1 in transposed_piece[1]:
#         chord = []
#         if type(chord1) == note.Rest:
#             chord = 'r'
#         else:
#             for c_note in chord1.pitches:
#                 chord.append(c_note.nameWithOctave)

#         chords.append(chord)

#     return transposed_piece, notes, chords


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
    parsed_input, numbers, notes = parse_melody(melody)
    chords = add_chords(numbers)

    for x in range(len(chords)):
        for n in range(len(chords[x])):
            if chords[x][n] != 'r':
                chords[x][n] += '3'

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
