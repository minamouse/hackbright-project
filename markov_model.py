from random import choice
import pickle


notes_to_chords = pickle.load(open('notes_to_chords.p', 'r'))
chords_to_chords = pickle.load(open('chords_to_chords.p', 'r'))
next_notes_to_chords = pickle.load(open('next_notes_to_chords.p', 'r'))


def get_downbeats(melody):

    events = []
    events.append((0.0, melody[0][1]))

    melody_length = melody[0][1]

    for i in melody[1:]:
        melody_length += i[1]
        events.append((events[-1][0] + events[-1][1], i[1]))

    new_melody = []

    for e, m in enumerate(melody):
        new_melody.append((m[0], m[1], events[e][0]))

    chord_notes = []
    chord_starts = []
    for m in new_melody:
        if m[1] >= 1 or m[2] % 1 == 0:
            chord_notes.append(m[0][:-1])
            chord_starts.append(m[2])

    chord_starts.append(melody_length)
    chord_lengths = []
    for e, c in enumerate(chord_starts[:-1]):
        chord_lengths.append(chord_starts[e+1] - c)

    return chord_notes, chord_lengths


def choose_chords(notes):

    chords = ['begin']
    notes.append('end')

    for m in range(len(notes)-1):

        if notes[m] in notes_to_chords:
            n_choice = notes_to_chords[notes[m]]
        else:
            n_choice = []

        if chords[-1] in chords_to_chords:
            c_choice = chords_to_chords[chords[-1]]
        else:
            c_choice = []

        if notes[m+1] in next_notes_to_chords:
            next_choice = next_notes_to_chords[notes[m+1]]
        else:
            next_choice = []

        choices = list(set(set(n_choice).intersection(c_choice)).intersection(next_choice))

        if not choices:
            choices = list(set(n_choice).intersection(c_choice))

        if not choices:
            choices = n_choice

        next_chord = choice(choices)
        chords.append(next_chord)

    return chords[1:]


def add_chords(melody):

    notes, lengths = get_downbeats(melody)
    chords = choose_chords(notes)
    return chords, lengths
