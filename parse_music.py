from music21 import stream, note, interval
from music21.pitch import PitchException


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.
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


if __name__ == "__main__":
    import doctest
    if not doctest.testmod().failed:
        print "\n*** ALL TESTS PASS ***\n"
