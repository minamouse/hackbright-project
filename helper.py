from parse_music import parse_melody, to_scale_degrees
from music21 import midi, interval, note
import fake_markov
import subprocess
import os


def transpose_back(piece, key):

    current_note = piece.analyze('key')
    current_note = note.Note(current_note.name[0])

    goal_note = note.Note(key.name[0])

    transpose_intvl = interval.notesToInterval(current_note, goal_note)
    transposed_piece = piece.transpose(transpose_intvl)

    notes = []
    for note1 in transposed_piece[0]:
        notes.append(note1.nameWithOctave)

    chords = []
    middle = note.Note('C3')

    for chord1 in transposed_piece[1]:
        chord = []
        highest = 0
        lowest = 0
        for c_note in chord1.pitches:

            chord.append(c_note.nameWithOctave)

        chords.append(chord)

    return transposed_piece, notes, chords


def new_song(melody, user_id=''):
    """ Creates a new song from a user input melody.
    """

    mid = 'static/song' + str(user_id) + '.mid'
    wav = 'static/song' + str(user_id) + '.wav'

    # turn melody string into music21 object and transpose
    parsed_input = parse_melody(melody)
    old_key = parsed_input.analyze('key')
    melody = to_scale_degrees(parsed_input)

    new_song, notes, chords = fake_markov.add_chords(melody)

    transposed_song, notes, chords = transpose_back(new_song, old_key)

    # new_song.write('lily.svg', fp='static/scores/song')

    # write to midi file
    mf = midi.translate.streamToMidiFile(transposed_song)
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
