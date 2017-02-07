from music21 import corpus, stream, chord, note, midi
from parse_music import to_scale_degrees, process_piece, parse_melody
from random import choice


def markov(data, note_dict={}):
    """ Create markov-chain-like dictionary from song data.
    """

    for key, value in data.values():
        if key and value:
            if key in note_dict:
                note_dict[key].append(value)
            else:
                note_dict[key] = [value]

    return note_dict


def add_chords(melody, note_dict):

    accomp = stream.Part()

    for nnote in melody:
        if nnote.name in note_dict:
            new_chord = list(choice(note_dict[nnote.name]))
            c = chord.Chord(new_chord)
        else:
            c = note.Rest()
        accomp.append(c)

    piece = stream.Stream()
    piece.append(melody)
    piece.append(accomp)
    return piece

melody = parse_melody("E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4")
piece = to_scale_degrees(corpus.parse('bach/bwv256.mxl'))
data = process_piece(piece)
chain = markov(data)

piece1 = add_chords(melody, chain)
st = midi.realtime.StreamPlayer(piece1)
st.play()
