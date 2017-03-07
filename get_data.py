from music21 import corpus, stream, note, chord
from pandas import DataFrame
import pickle


notes_to_chords = {}
chords_to_chords = {}
next_notes_to_chords = {}


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
                accompaniment[event.offset] = ' '.join(sorted(list(set([p.name for p in event.pitches]))))

    df = DataFrame([melody, accompaniment]).T.dropna()
    return df


def dataframe_to_features(df):

    for i in range(len(df)-1):

        note = df.loc[df.index[i]][0]
        chord = df.loc[df.index[i]][1]
        next_chord = df.loc[df.index[i+1]][1]
        next_note = df.loc[df.index[i+1]][0]

        if note in notes_to_chords:
            notes_to_chords[note].append(chord)
        else:
            notes_to_chords[note] = [chord]

        if chord in chords_to_chords:
            chords_to_chords[chord].append(next_chord)
        else:
            chords_to_chords[chord] = [next_chord]

        if next_note in next_notes_to_chords:
            next_notes_to_chords[next_note].append(chord)
        else:
            next_notes_to_chords[next_note] = [chord]

    i += 1
    note = df.loc[df.index[i]][0]
    chord = df.loc[df.index[i]][1]

    if note in notes_to_chords:
        notes_to_chords[note].append(chord)
    else:
        notes_to_chords[note] = [chord]

    if 'end' in next_notes_to_chords:
        next_notes_to_chords['end'].append(chord)
    else:
        next_notes_to_chords['end'] = [chord]


if __name__ == '__main__':

    paths = corpus.getComposer('bach')[:-20]
    for path in paths:

        # strip off the extra folder names in the path name
        pathname = path[82:]
        print '***Parsing', pathname + '***'

        df = parse_song(pathname)
        if df is not None:
            print '>>>'
            dataframe_to_features(df)

    pickle.dump(notes_to_chords, open('notes_to_chords.p', 'w'))
    pickle.dump(chords_to_chords, open('chords_to_chords.p', 'w'))
    pickle.dump(next_notes_to_chords, open('next_notes_to_chords.p', 'w'))
