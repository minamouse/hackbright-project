from sklearn.model_selection import train_test_split as ttsplit
from machine_learning import run_knn_test, run_gnb_test, run_rfc_test
from music21 import converter, stream, note, chord
from pandas import DataFrame
import pickle
import os


def convert_to_vector(notes):
    """ Given a list of midi values, create a vector describing it.
    """

    vector = [0 for x in range(15)]
    if 'r' in notes:
        vector[12] = 1
    else:
        for n in notes:
            vector[int(n)] = 1

    return vector


def parse_file(song_path):
    """ Given a song path, returns a pandas dataframe containing the
        piece's musical information.

        The output will have two columns, the first representing the melodic
        line and the second representing a list of the other notes occuring at
        that time in the piece.
    """

    try:
        song = converter.parse(song_path)
    except:
        print song_path, "wasn't parsed"
        return

    parts = []
    for part in song.getElementsByClass(stream.Part):
        part_dict = {}
        for measure in part.getElementsByClass(stream.Measure):
            measure.transferOffsetToElements()
            for event in measure:
                if type(event) == note.Note:
                    part_dict[event.offset] = event.pitch.midi % 12
                elif type(event) == note.Rest:
                    part_dict[event.offset] = 'r'
                elif type(event) == chord.Chord:
                    part_dict[event.offset] = event.pitchClasses

        parts.append(part_dict)

    df = DataFrame(parts).T.ffill().fillna('r')
    data = []
    for x in df.columns:
        data.append(df[x].tolist())

    melody = []
    rest = []
    for el in zip(*data):
        accomp = []
        if type(el[0]) == list:
            high_note = max(el[0])
            remaining = [e for e in el[0] if e != high_note]
            melody.append(high_note)
            accomp.extend(remaining)
        else:
            melody.append(el[0])

        for x in range(1, len(el)):
            if type(el[x]) == list:
                accomp.extend(el[x])
            else:
                accomp.append(el[x])

        accomp = set(accomp)
        if 'r' in accomp and len(accomp) > 1:
            accomp.remove('r')
        rest.append(sorted(list(accomp)))

    new_rest = []
    for r in rest:
        new_rest.append(convert_to_vector(r))

    begin_vector = [0 for x in range(15)]
    begin_vector[13] = 1
    end_vector = [0 for x in range(15)]
    end_vector[14] = 1
    melody.insert(0, 13)
    melody.append(14)
    new_rest.insert(0, begin_vector)
    new_rest.append(end_vector)

    new_df = DataFrame([melody, new_rest]).T
    return new_df.fillna('r')


def parse_all_files(directory='music_files/clementi'):
    songs = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            name = directory + '/' + f
            songs.append(parse_file(name))

    return songs


def get_data(df, window=2):
    """ Given a dataframe of song data and a window, get individual data points
        for features and labels.
    """
    features = []
    labels = []
    for i in range(len(df)-(window-1)):
        feat = []
        for x in range(i, i+(window-1)):
            if df.loc[x][0] == 'r':
                feat.append(12)
            else:
                feat.append(df.loc[x][0])
            feat.extend(df.loc[x][1])

        if df.loc[x+1][0] == 'r':
            feat.append(12)
        else:
            feat.append(df.loc[x+1][0])
        labels.append(df.loc[x+1][1])
        features.append(feat)

    return features, labels


def get_data_surround(df):
    """ Organizes features: the previous note, the previous chord, the current
        note and the next note in order to guess the current chord.
    """

    features = []
    labels = []

    for i in range(len(df)-2):
        feat = []
        if df.loc[i][0] == 'r':
            feat.append(12)
        else:
            feat.append(df.loc[i][0])
        feat.extend(df.loc[i][1])

        labels.append(df.loc[i+1][1])
        for x in range(1, 3):
            if df.loc[i+x][0] == 'r':
                feat.append(12)
            else:
                feat.append(df.loc[i+x][0])

        features.append(feat)

    return features, labels


if __name__ == '__main__':

    all_features = []
    all_labels = []
    all_dataframes = []

    dirs = ['music_files/beethoven', 'music_files/brahms', 'music_files/clementi',
            'music_files/corelli', 'music_files/haydn', 'music_files/hummel',
            'music_files/vivaldi', 'music_files/buxtehude']

    for d in dirs:
        print 'parsing files'
        all_dataframes.extend(parse_all_files())

    for df in all_dataframes:
        print 'creating features'
        features, labels = get_data_surround(df)
        all_features.extend(features)
        all_labels.extend(labels)

    label_convert = {}
    new_labels = []
    for l in all_labels:
        new_l = ''.join([str(x) for x in l])
        label_convert[new_l] = l
        new_labels.append(new_l)

    xtrain, xtest, ytrain, ytest = ttsplit(all_features, new_labels, test_size=0.33)

    print 'dumping to pickle files'
    pickle.dump(label_convert, open('convert_labels.p', 'wb'))
    pickle.dump(all_features, open('features.p', 'wb'))
    pickle.dump(new_labels, open('labels.p', 'wb'))

    print "finished create pickled files. quit the program to stop the tests from running."
    run_rfc_test(xtrain, ytrain, xtest, ytest)
    run_gnb_test(xtrain, ytrain, xtest, ytest)
    run_knn_test(xtrain, ytrain, xtest, ytest)
