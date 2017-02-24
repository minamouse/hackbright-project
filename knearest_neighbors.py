from sklearn.neighbors import KNeighborsClassifier
import pickle

features = pickle.load(open('features.p', 'rb'))
labels = pickle.load(open('labels.p', 'rb'))
convert_labels = pickle.load(open('convert_labels.p', 'rb'))

knn = KNeighborsClassifier(algorithm='kd_tree', n_neighbors=20, weights='distance')
knn.fit(features, labels)

note_names = {0: 'C',
              1: 'C#',
              2: 'D',
              3: 'E-',
              4: 'E',
              5: 'F',
              6: 'F#',
              7: 'G',
              8: 'A-',
              9: 'A',
              10: 'B-',
              11: 'B',
              12: 'r'}


def add_chords(melody):

    melody.insert(0, 13)
    melody.append(14)
    begin_vector = [0 for x in range(15)]
    begin_vector[13] = 1
    accompaniment = [begin_vector]

    for i in range(len(melody)-2):
        features = []
        features.append(melody[i])
        features.extend(accompaniment[-1])
        features.extend([melody[i+1], melody[i+2]])

        guess = knn.predict([features])

        accompaniment.append(convert_labels[guess[0]])

    chords = vector_to_chord(accompaniment[1:])
    return chords


def vector_to_chord(accompaniment):

    chords = []

    for vector in accompaniment:
        notes = [note_names[i] for i, x in enumerate(vector) if x == 1]
        chords.append(notes)

    return chords
