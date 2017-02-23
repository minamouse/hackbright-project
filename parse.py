from sklearn.model_selection import train_test_split as ttsplit
from machine_learning import run_knn, run_gnb, run_rfc
from music21 import converter, stream, note, chord
from sklearn import preprocessing
from pandas import DataFrame
import os


def convert_to_vector(notes):
    """ Given a list of midi values, create a vector describing it.
    """

    vector = [0 for x in range(13)]
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

    df = DataFrame(parts).T.ffill()
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

    new_df = DataFrame([melody, new_rest]).T
    return new_df.fillna('r')


def parse_all_files(directory='music_files/beethoven'):
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


parse_all_files('music_files/corelli')

# all_features = []
# all_labels = []

# parsed_files = parse_all_files()

# for df in parsed_files:
#     features, labels = get_data(df, 5)
#     all_features.extend(features)
#     all_labels.extend(labels)

# label_convert = {}
# new_labels = []
# for l in all_labels:
#     new_l = ''.join([str(x) for x in l])
#     label_convert[new_l] = l
#     new_labels.append(new_l)

# xtrain, xtest, ytrain, ytest = ttsplit(all_features, new_labels, test_size=0.33)

# run_rfc(xtrain, ytrain, xtest, ytest)
# run_gnb(xtrain, ytrain, xtest, ytest)
# run_knn(xtrain, ytrain, xtest, ytest)



# >>> from sklearn.datasets import make_classification
# >>> from sklearn.multioutput import MultiOutputClassifier
# >>> from sklearn.ensemble import RandomForestClassifier
# >>> from sklearn.utils import shuffle
# >>> import numpy as np
# >>> X, y1 = make_classification(n_samples=10, n_features=100, n_informative=30, n_classes=3, random_state=1)
# >>> y2 = shuffle(y1, random_state=1)
# >>> y3 = shuffle(y1, random_state=2)
# >>> Y = np.vstack((y1, y2, y3)).T
# >>> n_samples, n_features = X.shape # 10,100
# >>> n_outputs = Y.shape[1] # 3
# >>> n_classes = 3
# >>> forest = RandomForestClassifier(n_estimators=100, random_state=1)
# >>> multi_target_forest = MultiOutputClassifier(forest, n_jobs=-1)
# >>> multi_target_forest.fit(X, Y).predict(X)
# array([[2, 2, 0],
#        [1, 2, 1],
#        [2, 1, 0],
#        [0, 0, 2],
#        [0, 2, 1],
#        [0, 0, 2],
#        [1, 1, 0],
#        [1, 1, 1],
#        [0, 0, 2],
#        [2, 0, 0]])
