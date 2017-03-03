from random import choice
import pickle


notes_to_chords = pickle.load(open('notes_to_chords.p', 'r'))
chords_to_chords = pickle.load(open('chords_to_chords.p', 'r'))
next_notes_to_chords = pickle.load(open('next_notes_to_chords.p', 'r'))


def get_downbeats(melody):
    """Return the melody notes that should be used for the machine learning,
    and the length that the chords should be."""

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


def combine_lists(note_choice, chord_choice, next_note_choice):

    final_list = []
    possibilities = []

    l = set(note_choice).intersection(chord_choice)
    if l:
        l2 = l.intersection(next_note_choice)
        if l2:
            possibilities = l2
        else:
            possibilities = l
    else:
        possibilities = note_choice

    for p in possibilities:
        l = [p for x in range(note_choice.count(p))]
        l2 = [p for x in range(chord_choice.count(p))]
        l3 = [p for x in range(next_note_choice.count(p))]
        final_list.extend(l)
        final_list.extend(l2)
        final_list.extend(l3)

    return final_list


def choose_chords(raw_notes):
    """From the list of overlapping chords, choose the chord most likely to appear."""

    chords = ['begin']
    notes = raw_notes + ['end']

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

        choices = combine_lists(n_choice, c_choice, next_choice)

        next_chord = choice(choices)
        chords.append(next_chord)

    return chords[1:]


def add_chords(melody):

    notes, lengths = get_downbeats(melody)
    chords = choose_chords(notes)
    return chords, lengths
