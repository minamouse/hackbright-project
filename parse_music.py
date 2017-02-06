from music21 import stream, note, midi, interval
from music21.pitch import PitchException


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.

    for example:

        >>> type(parse_melody("E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4"))
        <class 'music21.stream.Stream'>

        >>> type(parse_melody("G4 Rest D4 G4 Rest D4 G4 D4 G4 B4 D5"))
        <class 'music21.stream.Stream'>
    """
    piece = stream.Stream()

    for item in melody.split():
        try:
            piece.append(note.Note(item))
        except PitchException:
            piece.append(note.Rest(item))

    # st = midi.realtime.StreamPlayer(piece)
    # st.play()

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
        raise Exception('You should not be inputting music is neither major nor minor.')

    transpose_intvl = interval.notesToInterval(note.Note(key_note_str), goal_note)
    transposed_piece = piece.transpose(transpose_intvl)
    return transposed_piece


if __name__ == "__main__":
    import doctest
    if not doctest.testmod().failed:
        print "\n*** ALL TESTS PASS ***\n"
