from music21 import stream, chord, note
from random import choice
import pickle


def markov(data):
    """ Add to pickled version of markov-chain-like dictionary taken from song data.
    """

    note_dict = pickle.load(open('notes.p', 'rb'))
    print note_dict
    for key, value in data.values():
        if key and value:
            if key in note_dict:
                note_dict[key].append(value)
            else:
                note_dict[key] = [value]

    pickle.dump(note_dict, open('notes.p', 'wb'))


def add_chords(melody, note_dict):
    """ Create chords based on likelihood and add them to the piece.
    """

    accomp = stream.Part()

    for nnote in melody:
        if nnote.name in note_dict:
            new_chord = list(choice(note_dict[nnote.name]))
            c = chord.Chord([n + '3' for n in new_chord])
        else:
            c = note.Rest()
        accomp.append(c)

    piece = stream.Stream()
    piece.append(melody)
    piece.append(accomp)
    return piece
