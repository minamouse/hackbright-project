from music21 import stream, note, interval, corpus, chord, midi
from music21.pitch import PitchException
from markov import markov, add_chords
import pickle


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.

    for example:

        >>> type(parse_melody("E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4"))
        <class 'music21.stream.Part'>

        >>> type(parse_melody("G4 Rest D4 G4 Rest D4 G4 D4 G4 B4 D5"))
        <class 'music21.stream.Part'>
    """
    piece = stream.Part()

    for item in melody.split():
        try:
            piece.append(note.Note(item))
        except PitchException:
            piece.append(note.Rest(item))

    return piece


def to_scale_degrees(piece):
    """ Given a music21 stream object, converts it to C major or a minor.

    for example:

        >>> song = parse_melody("E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4")
        >>> to_scale_degrees(song).analyze('key')
        <music21.key.Key of C major>

        >>> song = parse_melody("G4 G4 A-4 B-4 B-4 A-4 G4 F4 E-4 E-4 F4 G4 G4 F4 F4")
        >>> to_scale_degrees(song).analyze('key')
        <music21.key.Key of C major>

        >>> song = parse_melody("D4 F4 G4 A4 B-4 A4 G4 E4 C4 D4 E4 F4 D4 D4")
        >>> to_scale_degrees(song).analyze('key')
        <music21.key.Key of a minor>
    """

    key = piece.analyze('key')
    key_note_str = key.name.split()[0]

    if key.mode == 'major':
        goal_note = note.Note('C')

    elif key.mode == 'minor':
        goal_note = note.Note('A')

    else:
        raise Exception('Invalid music input: piece should be either major or minor.')

    transpose_intvl = interval.notesToInterval(note.Note(key_note_str), goal_note)
    transposed_piece = piece.transpose(transpose_intvl)
    return transposed_piece


def process_piece(piece):
    """ Given a piece, does the necessary processing to prepare it for ML.

    for example:
        >>> piece = to_scale_degrees(corpus.parse('demos/chorale_with_parallels.mxl'))
        >>> process_piece(piece)[0]
        ('E', set(['A', 'C']))
    """

    # removes stream objects that don't have notes -- textboxes or metadata
    for element in piece:
        if type(element) != stream.Part:
            piece.remove(element)

    melody = piece.pop(0)  # for now, the melody will always be in the top part
    piece = piece.chordify()

    # get all the measure elements
    melody_measures = [m for m in melody if type(m) == stream.Measure]
    measures = [m for m in piece if type(m) == stream.Measure]

    comb_dict = {}

    for m in melody_measures:
        m.transferOffsetToElements()

        for n in m:
            if type(n) == note.Note:
                comb_dict[n.offset] = (n.name, [])
            elif type(n) == note.Rest:
                comb_dict[n.offset] = ('Rest', [])

    for m in measures:
        m.transferOffsetToElements()

        for c in m:
            if type(c) == chord.Chord:
                notes = [n.name for n in c.pitches]
                if c.offset in comb_dict:
                    mel = comb_dict[c.offset][0]
                    if mel in notes:
                        notes.remove(mel)
                    comb_dict[c.offset] = (mel, set(notes))
                else:
                    comb_dict[c.offset] = (None, set(notes))

    return comb_dict


def parse_corpus():
    """ Get all the pieces from the music21 corpus of Bach pieces.

    This function will be replaced later, because the corpus here is too small
    to be ideal for machine learning.
    """

    print '*' * 20
    print 'parsing corpus'
    pieces = corpus.getComposer('bach')
    numbers = range(253, 438)
    numbers = [str(n) for n in numbers]
    for piece in pieces:
        if piece[-7:-4] in numbers:
            print '*' * 10
            print 'parsing piece ' + piece[-7:-4]
            piece = to_scale_degrees(corpus.parse(piece))
            note_dict = process_piece(piece)
            markov(note_dict)


# parsed_input = parse_melody("D4 F4 G4 A4 B-4 A4 G4 E4 C4 D4 E4 F4 D4 D4")
# melody = to_scale_degrees(parsed_input)

pickle.dump({}, open('notes.p', 'wb'))
complete_dict = parse_corpus()

# complete_dict = pickle.load(open('notes.p', 'rb'))

# new_song = add_chords(melody, complete_dict)
# st = midi.realtime.StreamPlayer(new_song)
# st.play()


if __name__ == "__main__":
    import doctest
    if not doctest.testmod().failed:
        print "\n*** ALL TESTS PASS ***\n"
