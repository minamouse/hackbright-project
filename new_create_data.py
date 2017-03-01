from music21 import corpus, chord, stream, note
from pandas import DataFrame
import pickle


names_to_numbers = {}
numbers_to_names = {}



def parse_file(song_path):
    """ Given a song path, returns a pandas dataframe containing the
        piece's musical information.

        The output will have two columns, the first representing the melodic
        line and the second representing a list of the other notes occuring at
        that time in the piece.
    """

    try:
        song = corpus.parse(song_path)
    except:
        print song_path, "wasn't parsed"
        return

    chords = song.chordify()

    parts = [p for p in song.getElementsByClass(stream.Part)]
    melody = {}
    for measure in parts[0].getElementsByClass(stream.Measure):
        measure.transferOffsetToElements()
        for event in measure:
            if event.offset % 1 == 0:
                if type(event) == note.Note:
                    melody[event.offset] = event.name + '/' + str(event.duration.quarterLength)
                elif type(event) == note.Rest:
                    melody[event.offset] = 'r' + '/' + str(event.duration.quarterLength)
                elif type(event) == chord.Chord:
                    chord_notes = sorted(event.pitches, key=lambda p: -p.midi)
                    melody[event.offset] = chord_notes[0].name + '/' + str(event.duration.quarterLength)

    accompaniment = {}
    for measure in chords.getElementsByClass(stream.Measure):
        measure.transferOffsetToElements()
        if event.offset % 1 == 0:
            for event in measure:
                event_name = []
                if type(event) == chord.Chord:
                    event_name = event.root().name + ' ' + event.quality
                    accompaniment[event.offset] = event_name

    df = DataFrame([melody, accompaniment]).T.dropna()
    return df


def dataframe_to_features(df):

    features = []

    if len(df) >= 2:
        feat = ['begin', 'begin', df.loc[df.index[0]][0], df.loc[df.index[1]][0]]
        features.append(feat)

        labels = [df.loc[df.index[0]][1]]
        i = 0
        for i in range(len(df.index)-2):
            feat = []
            feat.append(df.loc[df.index[i]][0])
            feat.append(df.loc[df.index[i]][1])
            feat.append(df.loc[df.index[i+1]][0])
            feat.append(df.loc[df.index[i+2]][0])

            features.append(feat)

            labels.append(df.loc[df.index[i+1]][1])

        i += 1
        feat = [df.loc[df.index[i]][0], df.loc[df.index[i]][1], df.loc[df.index[i+1]][0], 'end']
        features.append(feat)
        labels.append(df.loc[df.index[i+1]][1])

        return features, labels


all_dataframes = []

all_features = []
all_labels = []

for p in corpus.getComposer('bach')[:29]:
    path = p[94:]
    print path
    all_dataframes.append(parse_file(path))

x = 0
for df in all_dataframes:
    print x, len(all_dataframes)
    x += 1
    results = dataframe_to_features(df)
    if results:
        features, labels = results
        all_features.extend(features)
        all_labels.extend(labels)

number_labels = []
current_num = 0
for label in all_labels:

    if label not in names_to_numbers:
        names_to_numbers[label] = current_num
        numbers_to_names[current_num] = label
        current_num += 1

    number_labels.append(names_to_numbers[label])

number_features = []
for features in all_features:
    new_features = []
    for f in features:
        if f not in names_to_numbers:
            names_to_numbers[f] = current_num
            numbers_to_names[current_num] = f
            current_num += 1

        new_features.append(names_to_numbers[f])
    number_features.append(new_features)


pickle.dump(number_features, open('number_features.p', 'w'))
pickle.dump(number_labels, open('number_labels.p', 'w'))
pickle.dump(names_to_numbers, open('names_to_numbers.p', 'w'))
pickle.dump(numbers_to_names, open('numbers_to_names.p', 'w'))

# this will work well for list of notes, but not for named chords (major/minor)
# for p in corpus.getComposer('ryansMammoth'):
#     path = p[94:]
#     parse_file(path)
