import pickle
from random import choice


data = pickle.load(open('data.p', 'r'))
print data


def add_chords(melody):

    chords = ['begin']
    melody.insert(0, 'begin')

    for i in range(len(melody)-1):
        if type(chords[-1]) == list:
            chord = ' '.join(chords[-1])
        else:
            chord = chords[-1]
        features = ' '.join([melody[i], chord, melody[i+1]])
        label = choice(data[features])
        chords.append(label)

    return chords
