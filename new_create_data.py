from music21 import converter, chord, stream, note
from pandas import DataFrame


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

    # chords = song.chordify()
    # all_events = {}

    # for measure in chords.getElementsByClass(stream.Measure):
    #     measure.transferOffsetToElements()
    #     for event in measure:
    #         if type(event) == chord.Chord:
    #             print event.offset, event.duration.quarterLength,
    #             chord_notes = [p.nameWithOctave for p in sorted(event.pitches, key=lambda p: -p.midi)]
    #             melody = chord_notes[0]
    #             accomp = chord.Chord(chord_notes[1:]).closedPosition(forceOctave=3)
    #             accomp = [p.nameWithOctave for p in sorted(accomp.pitches, key=lambda p: -p.midi)]
    #             all_events[event.offset] = [event.duration.quarterLength, melody, chord_notes[1:], accomp]

    # df = DataFrame(all_events)
    # print df.T

    parts = [p for p in song.getElementsByClass(stream.Part)]
    melody = {}
    for measure in parts[0].getElementsByClass(stream.Measure):
        measure.transferOffsetToElements()
        for event in measure:
            if type(event) == note.Note:
                melody[event.offset] = event.name, event.duration.quarterLength
            elif type(event) == note.Rest:
                melody[event.offset] = 'r', event.duration.quarterLength
            elif type(event) == chord.Chord:
                chord_notes = sorted(event.pitches, key=lambda p: -p.midi)
                melody[event.offset] = [p.name for p in chord_notes], event.duration.quarterLength

    accompaniment = {}
    for part in parts[1:]:
        for measure in part.getElementsByClass(stream.Measure):
            measure.transferOffsetToElements()
            for event in measure:
                event_name = []
                if type(event) == note.Note:
                    event_name = [event.name]
                elif type(event) == note.Rest:
                    event_name = ['r']
                elif type(event) == chord.Chord:
                    event_name = [p.name for p in event.pitches]

                if event.offset in accompaniment:
                    accompaniment[event.offset].extend(event_name)
                else:
                    accompaniment[event.offset] = event_name

    for offset in accompaniment:
        new_chord = chord.Chord(accompaniment[offset])
        notes = [n.name for n in new_chord.closedPosition().pitches]
        accompaniment[offset] = notes
    df = DataFrame([melody, accompaniment]).T
    # df[1] = df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(int).astype(str)), axis=1)
    print df
    # for part in song.getElementsByClass(stream.Part):
    #     part_dict = {}
    #     for measure in part.getElementsByClass(stream.Measure):
    #         measure.transferOffsetToElements()
    #         for event in measure:
    #             if type(event) == note.Note:
    #                 part_dict[event.offset] = event.name, event.duration.quarterLength
    #             elif type(event) == note.Rest:
    #                 part_dict[event.offset] = 'r'
    #             elif type(event) == chord.Chord:
    #                 part_dict[event.offset] = [p.nameWithOctave for p in event.pitches]

    #     parts.append(part_dict)

    # df = DataFrame(parts).T.dropna(subset=[0]).fillna('continue')
    # print df

    # data = []
    # for x in df.columns:
    #     data.append(df[x].tolist())

    # melody = []
    # rest = []
    # for el in zip(*data):
    #     accomp = []
    #     if type(el[0]) == list:
    #         high_note = max(el[0])
    #         remaining = [e for e in el[0] if e != high_note]
    #         melody.append(high_note)
    #         accomp.extend(remaining)
    #     else:
    #         melody.append(el[0])

    #     for x in range(1, len(el)):
    #         if type(el[x]) == list:
    #             accomp.extend(el[x])
    #         else:
    #             accomp.append(el[x])

    #     accomp = set(accomp)
    #     if 'r' in accomp and len(accomp) > 1:
    #         accomp.remove('r')
    #     rest.append(sorted(list(accomp)))

    # new_rest = []
    # for r in rest:
    #     new_rest.append(convert_to_vector(r))

    # begin_vector = [0 for x in range(15)]
    # begin_vector[13] = 1
    # end_vector = [0 for x in range(15)]
    # end_vector[14] = 1
    # melody.insert(0, 13)
    # melody.append(14)
    # new_rest.insert(0, begin_vector)
    # new_rest.append(end_vector)

    # new_df = DataFrame([melody, new_rest]).T
    # return new_df.fillna('r')

parse_file('music_files/corelli/op01n01a.krn')
