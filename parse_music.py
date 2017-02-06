from music21 import stream, note, midi


def parse_melody(melody):
    """Takes in a string of note names and returns a music21 object.

    for example:
        >>> type(parse_melody("E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4"))
        <class 'music21.stream.Stream'>

    """
    song = stream.Stream()

    for item in melody.split():
        song.append(note.Note(item))

    return song

if __name__ == "__main__":
    import doctest
    if not doctest.testmod().failed:
        print "\n*** ALL TESTS PASS ***\n"
