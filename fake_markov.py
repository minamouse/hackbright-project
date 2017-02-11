from music21 import corpus, chord, note, stream
from random import choice
import pickle


pieces = []
PICKLE_FILE = 'notes.p'


def get_bach_pieces():
    """ Converts the necessary pieces into music21 objects.

    In this case, it parses all the bach chorales from the music21 sample corpus.
    """

    all_bach_pieces = corpus.getComposer('bach')

    bwv_numbers = [str(n) for n in range(253, 438)]

    for piece in all_bach_pieces:
        if piece[-7:-4] in bwv_numbers:

            print '*' * 10
            print 'parsing piece ' + piece[-7:-4]
            print '*' * 10 + '\n'

            pieces.append(corpus.parse(piece))


def process_piece(piece, mel_part):
    """ Given a piece, does the necessary processing to prepare it for ML.
    """

    # removes stream objects that don't have notes -- textboxes or metadata
    for element in piece:
        if type(element) != stream.Part:
            piece.remove(element)

    melody = piece.pop(mel_part)
    piece = piece.chordify()

    # get all the measure elements
    melody_measures = [m for m in melody if type(m) == stream.Measure]
    measures = [m for m in piece if type(m) == stream.Measure]

    comb_dict = {}

    for m in melody_measures:
        m.transferOffsetToElements()

        for n in m:
            if type(n) == note.Note:
                comb_dict[n.offset] = (n.nameWithOctave, [])
            elif type(n) == note.Rest:
                comb_dict[n.offset] = ('Rest', [])

    for m in measures:
        m.transferOffsetToElements()
        for c in m:
            if type(c) == chord.Chord:
                notes = [n.nameWithOctave for n in c.pitches]
                if c.offset in comb_dict:
                    mel = comb_dict[c.offset][0]
                    if mel in notes:
                        notes.remove(mel)
                    comb_dict[c.offset] = (mel, set(notes))
                else:
                    comb_dict[c.offset] = (None, set(notes))

    return comb_dict


def create_pickled_file():
    """ Use this function to create a pickle file for the sample corpus.
    """

    # whether or not you have a PICKLE_FILE file, this will add only an empty
    # dictionary to it. This is useful for initializing the pickle file later,
    # but overwrites anything you might already have in your file so be careful!
    pickle.dump({}, open(PICKLE_FILE, 'wb'))


def markov(data):
    """ Add to pickled version of markov-chain-like dictionary taken from song data.
    """

    note_dict = pickle.load(open(PICKLE_FILE, 'rb'))

    for key, value in data.values():
        if key and value:
            if key in note_dict:
                note_dict[key].append(value)
            else:
                note_dict[key] = [value]

    pickle.dump(note_dict, open(PICKLE_FILE, 'wb'))


def add_chords(melody):
    """ Create chords based on likelihood and add them to the piece.
    """

    note_dict = pickle.load(open(PICKLE_FILE, 'rb'))

    accomp = stream.Part()

    for nnote in melody:
        if nnote.nameWithOctave in note_dict:
            new_chord = list(choice(note_dict[nnote.nameWithOctave]))
            # c = chord.Chord([n + '3' for n in new_chord])
            c = chord.Chord(new_chord)
        else:
            c = note.Rest()
        accomp.append(c)

    piece = stream.Stream()
    piece.append(melody)
    piece.append(accomp)
    return piece


if __name__ == '__main__':
    """If this file is run directly it will run the machine learning algorithm
    and add the data to the associated pickle file.
    """
    from parse_music import to_scale_degrees

    get_bach_pieces()

    create_pickled_file()

    for piece in pieces:
        transposed_piece = to_scale_degrees(piece)
        chord_dict = process_piece(transposed_piece, 0)
        markov(chord_dict)
