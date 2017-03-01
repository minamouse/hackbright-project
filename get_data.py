from music21 import corpus, stream, note, chord
from pandas import DataFrame
import pickle


def parse_song(path):

    try:
        song = corpus.parse(path)
    except:
        print path, "couldn't be parsed"
        return

    chords = song.chordify()

    parts = [p for p in song.getElementsByClass(stream.Part)]
    melody = {-1: 'begin'}
    for measure in parts[0].getElementsByClass(stream.Measure):
        measure.transferOffsetToElements()
        for event in measure:
            if type(event) == note.Note:
                melody[event.offset] = event.name
            elif type(event) == note.Rest:
                melody[event.offset] = 'r'
            elif type(event) == chord.Chord:
                chord_notes = sorted(event.pitches, key=lambda p: -p.midi)
                melody[event.offset] = chord_notes[0].name

    accompaniment = {-1: 'begin'}
    for measure in chords.getElementsByClass(stream.Measure):
        measure.transferOffsetToElements()
        for event in measure:
            if type(event) == chord.Chord:
                print dir(event)
                accompaniment[event.offset] = event

    df = DataFrame([melody, accompaniment]).T.dropna()
    return df


def dataframe_to_features(df, giant_dictionary):

    for i in range(len(df)-1):
        features = ' '.join([df.loc[df.index[i]][0], df.loc[df.index[i]][1], df.loc[df.index[i+1]][0]])
        label = df.loc[df.index[i+1]][1]
        if features in giant_dictionary:
            giant_dictionary[features].append(label)
        else:
            giant_dictionary[features] = [label]

    return giant_dictionary


if __name__ == '__main__':

    giant_dictionary = {}

    paths = corpus.getComposer('bach')[:20]
    for path in paths:

        print '***Parsing', path[94:] + '***'

        # strip off the extra folder names in the path name
        df = parse_song(path[94:])
        giant_dictionary = dataframe_to_features(df, giant_dictionary)

    pickle.dump(giant_dictionary, open('data.p', 'w'))
